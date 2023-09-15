package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
)

type Address struct {
	Number int `json:"number"`
	Road string `json:"road"`
	City string `json:"city"`
	Postcode string `json:"postcode"`
}

type Person struct {
	Name string `json:"name"`
	Age int `json:"age"`
	Weight float64 `json:"weight"`
	Addresses []Address `json:"addresses"`
}

func readConfig(filepath string) (*Person, error) {

	file, err := os.Open(filepath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	content, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}

	var person Person
	err = json.Unmarshal(content, &person)
	if err != nil {
		return nil, err
	}

	return &person, nil
}

func main() {

	// Read the JSON config file from disk
	person, err := readConfig("./config1.json")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Person: %v\n", person)

	// Write to a JSON string
	bytes, err := json.Marshal(person)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Marshalled: %v\n", string(bytes))

	// Convert to a map[string]interface{}
	var generic map[string]interface{}
	bytes, err = json.Marshal(person)
	if err != nil {
		log.Fatal(err)
	}
	if err := json.Unmarshal(bytes, &generic); err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Generic: %v\n", generic)

	// Write the generic to a JSON string
	bytes, err = json.Marshal(generic)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Marshalled generic: %v\n", string(bytes))
}