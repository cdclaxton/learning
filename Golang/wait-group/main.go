package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

func doCalculation(x float64, y float64, pFailure float64) (float64, error) {
	time.Sleep(time.Second)
	if rand.Float64() < pFailure {
		return 0.0, fmt.Errorf("failed to calculate sum")
	}
	return x + y, nil
}

func main() {
	numCalculations := 5
	pFailure := 0.4

	// Single threaded
	// for i := range numCalculations {
	// 	x := rand.Float64()
	// 	y := rand.Float64()

	// 	result, err := doCalculation(x, y, pFailure)
	// 	if err != nil {
	// 		fmt.Printf("%d: failed\n", i)
	// 	} else {
	// 		fmt.Printf("%d: %f + %f = %f\n", i, x, y, result)
	// 	}
	// }

	// Multi-threaded
	results := make(chan string, numCalculations)
	errors := make(chan string, numCalculations)
	var wg sync.WaitGroup
	for i := range numCalculations {
		wg.Add(1)
		go func(j int, wg *sync.WaitGroup) {

			x := rand.Float64()
			y := rand.Float64()

			result, err := doCalculation(x, y, pFailure)
			if err != nil {
				errors <- fmt.Sprintf("%d: failed", j)
			} else {
				results <- fmt.Sprintf("%d: %f + %f = %f", i, x, y, result)
			}
			wg.Done()
		}(i, &wg)
	}

	wg.Wait()
	close(results)
	close(errors)

	if len(errors) > 0 {
		fmt.Printf("There are %d errors ...\n", len(errors))
	}

	for err := range errors {
		fmt.Println(err)
	}

	for result := range results {
		fmt.Println(result)
	}
}
