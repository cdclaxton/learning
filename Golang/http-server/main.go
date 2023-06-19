package main

import (
	"fmt"
	"net/http"
	"os"
	"os/signal"
)

func simpleHandler(w http.ResponseWriter, req *http.Request) {
	fmt.Printf("Received HTTP request: host=%v, URL=%v\n", req.Host, req.URL)
	fmt.Fprintf(w, "Hello!\n")
}

func startServer() {
	fmt.Println("Starting HTTP server ...")
	http.HandleFunc("/", simpleHandler)
	http.ListenAndServe(":8090", nil)
}

func main() {

	go startServer()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit)
	fmt.Println("Waiting for close ...")

	sig := <-quit
	fmt.Printf("\nSignal received: %v\n", sig)
}
