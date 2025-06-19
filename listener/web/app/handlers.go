package app

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"runtime"
	"strings"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"github.com/gofiber/fiber/v3"
)

var topics = map[string][]string{
	"open":    make([]string, 0),
	"call":    make([]string, 0),
	"buttons": make([]string, 0),
}

var lastCall = ""

func openbrowser(url string) {
	var err error
	switch runtime.GOOS {
	case "linux":
		err = exec.Command("xdg-open", url).Start()
	case "windows":
		err = exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
	case "darwin":
		err = exec.Command("open", url).Start()
	default:
		err = fmt.Errorf("unsupported platform")
	}
	if err != nil {
		log.Fatal(err)
	}
}

// define a function for the default message handler
var f mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
	topic := msg.Topic()
	payload := string(msg.Payload())

	if strings.Compare(string(payload), "\n") > 0 {
		topics[topic] = append(topics[topic], payload)
		fmt.Printf("TOPIC: %s\n", topic)
		fmt.Printf("MSG: %s\n", payload)
		if topic == "call" {
			openbrowser("http://127.0.0.1:3000/call")
			lastCall = payload
		}
	}
}

func getMqttOptions() *mqtt.ClientOptions {
	opts := mqtt.NewClientOptions().AddBroker("tcp://m4.wqtt.ru:13408")
	opts.SetClientID("Device-pub")
	opts.SetUsername("u_FAVYQ5")
	opts.SetPassword("Fa3sAjwH")
	opts.SetDefaultPublishHandler(f)
	return opts
}

func createClient(topics []string) {
	client := mqtt.NewClient(getMqttOptions())
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
	for _, topic := range topics {
		if topic == "call" {
			if token := client.Subscribe(topic, 0, nil); token.Wait() && token.Error() != nil {
				fmt.Println(token.Error())
				os.Exit(1)
			}
		}
		if token := client.Subscribe(topic, 0, nil); token.Wait() && token.Error() != nil {
			fmt.Println(token.Error())
			panic(token.Error())
		}
	}
}

func IndexHandler(c fiber.Ctx) error {
	return c.Render("index", fiber.Map{
		"topics": topics,
	})
}

func TopicOpenHandler(c fiber.Ctx) error {
	return c.Render("topic_info", fiber.Map{
		"topic":    "open",
		"messages": topics["open"],
	})
}

func TopicButtonsHandler(c fiber.Ctx) error {
	return c.Render("topic_info", fiber.Map{
		"topic":    "buttons",
		"messages": topics["buttons"],
	})
}

func TopicCallHandler(c fiber.Ctx) error {
	return c.Render("topic_info", fiber.Map{
		"topic":    "call",
		"messages": topics["call"],
	})
}

func GetCallHandler(c fiber.Ctx) error {

	return c.Render("call", fiber.Map{
		"lastCall": lastCall,
	})
}

func PostCallHandler(c fiber.Ctx) error {
	// доделай
	return c.Render("call", fiber.Map{
		"lastCall": lastCall,
	})
}
