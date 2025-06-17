package app

import (
	"fmt"
	"os"
	"strings"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
	"github.com/gofiber/fiber/v3"
)

var flag bool = false

// define a function for the default message handler
var f mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
	topic := msg.Topic()
	payload := msg.Payload()
	if strings.Compare(string(payload), "\n") > 0 {
		fmt.Printf("TOPIC: %s\n", topic)
		fmt.Printf("MSG: %s\n", payload)
	}

	if strings.Compare("bye\n", string(payload)) == 0 {
		fmt.Println("exitting")
		flag = true
	}
}

func IndexHandler(c fiber.Ctx) error {
	opts := mqtt.NewClientOptions().AddBroker("tcp://m4.wqtt.ru:13408")

	// set the id to the client.
	opts.SetClientID("Device-pub")
	opts.SetUsername("u_FAVYQ5")
	opts.SetPassword("Fa3sAjwH")
	opts.SetDefaultPublishHandler(f)
	// create a new client.
	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
	if token := client.Subscribe("buttons", 0, nil); token.Wait() && token.Error() != nil {
		fmt.Println(token.Error())
		os.Exit(1)
	}
	for flag == false {
		time.Sleep(1 * time.Second)
		//fmt.Println("waiting: ", wcount)
		//wcount += 1
	}
	return c.Render("index", fiber.Map{})

}
