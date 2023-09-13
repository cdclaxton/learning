package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
)

// readJsonFile reads a JSON file from disk.
func readJsonFile(filepath string) (map[string]interface{}, error) {

	// Read the contents of the JSON file
	file, err := os.Open(filepath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	content, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}

	// Unmarshall the data
	var data map[string]interface{}
	err = json.Unmarshal(content, &data)
	if err != nil {
		return nil, err
	}

	return data, nil
}

func merge(p1, p2 map[string]interface{}) (map[string]interface{}, error) {

	result := map[string]interface{}{}

	for key, value := range p1 {
		result[key] = value
	}

	for key, value := range p2 {
		_, ok := result[key]
		if ok {
			return nil, fmt.Errorf("Key '%s' already exists", key)
		}

		result[key] = value
	}

	return result, nil
}

func main() {

	// Read the two JSON files
	file1, err := readJsonFile("config1.json")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("File 1: %v\n", file1)

	file2, err := readJsonFile("config2.json")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("File 2: %v\n", file2)

	// Perform the merge
	result, err := merge(file1, file2)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Merged: %v\n", result)
}