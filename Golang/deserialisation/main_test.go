package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestReadConfig(t *testing.T) {
	config, err := readJson("./test-data/config-1.json")
	assert.NoError(t, err)

	expected := Config{
		Name: "a",
		Data: map[string]interface{}{
			"field1": "b",
			"field2": "c",
		},
	}

	assert.Equal(t, expected, *config)
}

func TestParseData(t *testing.T) {
	config := map[string]interface{}{
		"field1": "b",
		"field2": "c",
	}

	expected := TypeAConfig{
		Field1: "b",
		Field2: "c",
	}

	result, err := parseFields(config)
	assert.NoError(t, err)
	assert.NotNil(t, result)
	assert.Equal(t, expected, *result)
}
