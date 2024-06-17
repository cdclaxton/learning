package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/cdclaxton/protobuf-example/client"
	"github.com/cdclaxton/protobuf-example/server"
)

func main() {

	if len(os.Args) != 3 {
		fmt.Printf("Usage: %s [server|client] <server address>\n", os.Args[0])
		fmt.Printf("e.g. %s server localhost:5000\n", os.Args[0])
		return
	}

	// Address on which to listen
	addr := os.Args[2]

	stopService := make(chan os.Signal, 1)
	signal.Notify(stopService, syscall.SIGINT, syscall.SIGTERM)

	if os.Args[1] == "server" {
		s := server.NewServer(addr)
		if err := s.Start(); err != nil {
			fmt.Printf("Error starting server: %v\n", err)
		}

		fmt.Printf("Server started on %s\n", s.ListenAddress)
		fmt.Println("Press Ctrl+C to stop")

		<-stopService
		s.Stop()

	} else if os.Args[1] == "client" {
		c := client.NewClient(123, addr)
		if err := c.ConnectToServer(); err != nil {
			fmt.Printf("Error connecting to server: %v\n", err)
			return
		}

		if err := c.SendRegistrationRequest(); err != nil {
			fmt.Printf("Error sending registration request: %v\n", err)
			return
		} else {
			fmt.Println("Registration request sent")
		}

		if err := c.SendStatus(); err != nil {
			fmt.Printf("Error sending status: %v\n", err)
			return
		} else {
			fmt.Println("Status sent")
		}

	} else {
		fmt.Printf("Unknown command: %s\n", os.Args[1])
	}
}
