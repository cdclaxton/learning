// To build: `go build`

package main

import (
	"fmt"
	"time"
)

// expensiveOperation is a function that simulates a time intensive operation.
func expensiveOperation(idx int, delay int, shouldFail bool) error {
	time.Sleep(time.Duration(delay) * time.Second)
	if shouldFail {
		return fmt.Errorf("operation %d failed", idx)
	}
	return nil
}

// sequential run of two expensive operations.
func sequential(fail1 bool, fail2 bool) error {
	err := expensiveOperation(1, 1, fail1)
	if err != nil {
		return err
	}

	return expensiveOperation(2, 2, fail2)
}

// firstError given two errors.
func firstError(err1 error, err2 error) error {
	if err1 != nil {
		return err1
	}

	return err2
}

// concurrent running of two expensive operations
func concurrent(fail1 bool, fail2 bool) error {

	r1 := make(chan error)
	r2 := make(chan error)

	go func() {
		e1 := expensiveOperation(1, 1, fail1)
		r1 <- e1
	}()

	go func() {
		e2 := expensiveOperation(2, 2, fail2)
		r2 <- e2
	}()

	return firstError(<-r1, <-r2)
}

func main() {
	fmt.Println("Experiment with multiple concurrent processes")

	fail1 := true
	fail2 := false

	// Sequential approach
	err := sequential(fail1, fail2)
	fmt.Printf("Result from sequential: %v\n", err)

	// Concurrent approach
	err = concurrent(fail1, fail2)
	fmt.Printf("Result from concurrent: %v\n", err)
}
