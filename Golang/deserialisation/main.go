package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
)

type Config struct {
	Name string                 `json:"name"`
	Data map[string]interface{} `json:"data"`
}

type TypeAConfig struct {
	Field1 string `json:"field1"`
	Field2 string `json:"field2"`
}

func parseFields(config map[string]interface{}) (*TypeAConfig, error) {

	// Map the config back to JSON
	bytes, err := json.Marshal(config)
	if err != nil {
		return nil, err
	}

	t := TypeAConfig{}
	err = json.Unmarshal(bytes, &t)
	if err != nil {
		return nil, err
	}

	return &t, err
}

func readJson(filepath string) (*Config, error) {

	file, err := os.Open(filepath)
	if err != nil {
		return nil, err
	}

	content, err := io.ReadAll(file)
	if err != nil {
		return nil, err
	}

	var config Config
	err = json.Unmarshal(content, &config)
	if err != nil {
		return nil, err
	}

	return &config, nil
}

func main() {
	fmt.Println("Deserialisation")
}
