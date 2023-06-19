package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func processSignal(sigs <-chan os.Signal, done chan<- bool) {
	sig := <-sigs
	fmt.Printf("\nReceived signal: %v\n", sig)
	done <- true
}

func main() {

	// Create and register a channel to receive notifications
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	done := make(chan bool, 1)

	// Run a goroutine to process the signal
	go processSignal(sigs, done)

	fmt.Println("Awaiting signal ...")
	<-done
	fmt.Println("Exiting")
}
