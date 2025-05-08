package cmd

import (
	"fmt"
	"math"
	"strconv"
)

func parseTwoValues(first string, second string) (float64, float64, error) {
	num1, err := strconv.ParseFloat(first, 64)
	if err != nil {
		return 0.0, 0.0, fmt.Errorf("error: failed to parse first value")
	}

	num2, err := strconv.ParseFloat(second, 64)
	if err != nil {
		return 0.0, 0.0, fmt.Errorf("error: failed to parse second value")
	}

	return num1, num2, nil
}

func Add(first string, second string, roundNumber bool) (float64, error) {
	num1, num2, err := parseTwoValues(first, second)
	if err != nil {
		return 0.0, err
	}

	total := num1 + num2

	if roundNumber {
		total = math.Round(total)
	}

	return total, nil
}

func Subtract(first string, second string, roundNumber bool) (float64, error) {
	num1, num2, err := parseTwoValues(first, second)
	if err != nil {
		return 0.0, err
	}

	total := num1 - num2

	if roundNumber {
		total = math.Round(total)
	}

	return total, nil
}
