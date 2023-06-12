package main

import (
	"fmt"
	"log"
	"os"
)

func main() {

	// Set an environment variable
	err := os.Setenv("foo", "1")
	if err != nil {
		log.Fatal(err)
	}

	// Get environment variables
	fmt.Printf("foo: %s\n", os.Getenv("foo"))
	fmt.Printf("bar: %s\n", os.Getenv("bar"))

	// Get a system environment variable
	fmt.Printf("user: %s\n", os.Getenv("USER"))
}
