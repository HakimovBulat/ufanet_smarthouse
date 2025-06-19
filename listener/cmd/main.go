package main

import (
	"listener/web/app"
	"log"
)

func main() {
	app := app.Setup()
	log.Fatal(app.Listen(":3000"))
}
