package app

import (
	"log"

	"github.com/gofiber/fiber/v3"
	"github.com/gofiber/template/html/v2"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var db *gorm.DB

func Setup() *fiber.App {
	// pc, _, _, _ := runtime.Caller(1)
	engine := html.New("./web/templates", ".html")

	dsn := "host=localhost user=postgres password=postgres dbname=postgres port=5432 sslmode=disable"
	var err error
	db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal(err)
	}

	app := fiber.New(fiber.Config{
		Views: engine,
	})

	app.Get("/", IndexHandler)
	return app
}
