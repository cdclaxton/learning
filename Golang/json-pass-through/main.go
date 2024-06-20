package main

import (
	"encoding/json"
	"io"
	"log"
	"os"
)

type Person struct {
	Name    string                 `json:"name"`
	Age     int                    `json:"age"`
	Details map[string]interface{} `json:"details"`
}

type PersonEntity struct {
	Name    string                 `json:"person-name"`
	Age     int                    `json:"person-age"`
	Details map[string]interface{} `json:"person-details"`
}

func readPersonFromJson(filepath string) (*Person, error) {

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

func mapPersonToPersonEntity(person *Person) *PersonEntity {
	if person == nil {
		return nil
	}

	return &PersonEntity{
		Name:    person.Name,
		Age:     person.Age,
		Details: person.Details,
	}
}

func writePersonEntityToJson(personEntity *PersonEntity, filepath string) {

	bytes, err := json.Marshal(personEntity)
	if err != nil {
		log.Fatal(err)
	}

	f, err := os.Create(filepath)
	if err != nil {
		log.Fatal(err)
	}

	_, err = f.Write(bytes)
	if err != nil {
		log.Fatal(err)
	}
}

func main() {
	// Read the JSON file
	person, err := readPersonFromJson("./test-data/config-1.json")
	if err != nil {
		log.Fatal(err)
	}

	// Map a Person to a PersonEntity
	personEntity := mapPersonToPersonEntity(person)

	// Write a PersonEntity to a JSON file
	writePersonEntityToJson(personEntity, "./test-data/output-1.json")
}
