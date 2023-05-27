// Contexts
//
// A number of files are to be read from disk where each file contains one or
// more lines of data. If one line from one file cannot be read and parsed
// correctly, the program should stop as soon as the problem occurs. The files
// can be read concurrently.
//
// In this example code the focus is on how to stop the file reading as soon
// as a random error occurs.

package main

import (
	"context"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

type SyntheticFile struct {
	NumberOfLines int
	HasError      bool
	LineWithError int
}

// generateSyntheticFile with a random number of lines and a possible error on one line.
func generateSyntheticFile(minNumberLines int, maxNumberLines int, probabilityOfError float64) SyntheticFile {
	if minNumberLines < 0 {
		panic(fmt.Sprintf("invalid minium number of lines: %d\n", minNumberLines))
	}

	if maxNumberLines < minNumberLines {
		panic(fmt.Sprintf("invalid maximum number of lines: %d\n", maxNumberLines))
	}

	if probabilityOfError < 0.0 || probabilityOfError > 1.0 {
		panic(fmt.Sprintf("invalid probability: %f\n", probabilityOfError))
	}

	// Randomly select the number of lines in the file
	numberOfLines := rand.Intn(maxNumberLines-minNumberLines) + minNumberLines

	// Randomly determine if the file has an error and if so, on which line
	hasError := false
	lineWithError := -1
	if rand.Float64() < probabilityOfError {
		hasError = true
		lineWithError = rand.Intn(numberOfLines)
	}

	if numberOfLines < minNumberLines || numberOfLines > maxNumberLines {
		panic(fmt.Sprintf("invalid number of lines: %d\n", numberOfLines))
	}

	if hasError && lineWithError >= numberOfLines {
		panic(fmt.Sprintf("invalid line with error: %d (number of lines: %d)\n",
			lineWithError, numberOfLines))
	}

	return SyntheticFile{
		NumberOfLines: numberOfLines,
		HasError:      hasError,
		LineWithError: lineWithError,
	}
}

// makeSyntheticFiles makes num synthetic files.
func makeSyntheticFiles(num int, minNumberLines int, maxNumberLines int,
	probabilityOfError float64) []SyntheticFile {

	if num < 0 {
		panic(fmt.Sprintf("invalid number of files: %d", num))
	}

	files := make([]SyntheticFile, num)
	for i := 0; i < num; i++ {
		files[i] = generateSyntheticFile(minNumberLines, maxNumberLines, probabilityOfError)
	}

	return files
}

// singleThreadedRead reads each file one-by-one until an error occurs.
func singleThreadedRead(files []SyntheticFile) {
	for idx, file := range files {
		fmt.Printf("Starting to read file %d\n", idx)

		for lineNumber := 0; lineNumber < file.NumberOfLines; lineNumber++ {
			if file.HasError && file.LineWithError == lineNumber {
				fmt.Printf("ERROR: File %d has error on line %d\n", idx, lineNumber)
				return
			}

			fmt.Printf("Read line %d in file %d\n", lineNumber, idx)
		}
		fmt.Printf("Finished reading file %d\n", idx)
	}
}

func processFile(wg *sync.WaitGroup, ctx context.Context, cancelCtx context.CancelFunc,
	idx int, file SyntheticFile, errChannel chan<- string) {

	defer wg.Done()
	fmt.Printf("Processing file %d\n", idx)

	for lineNumber := 0; lineNumber < file.NumberOfLines; lineNumber++ {

		// Check to see if thejob should be prematurely ended
		select {
		case <-ctx.Done():
			if err := ctx.Err(); err != nil {
				fmt.Printf("File reader %d, ctx error: %s\n", idx, err)
			}
			return
		default:
		}

		if file.HasError && file.LineWithError == lineNumber {
			msg := fmt.Sprintf("ERROR: File %d has error on line %d\n", idx, lineNumber)
			fmt.Printf(msg)
			errChannel <- msg
			cancelCtx()
			return
		}

		fmt.Printf("Read line %d / %d in file %d\n", lineNumber, file.NumberOfLines-1, idx)
		time.Sleep(500 * time.Millisecond)
	}

}

func concurrentRead(files []SyntheticFile) {
	fmt.Println("\nConcurrent read ...")

	var wg sync.WaitGroup
	ctx := context.Background()
	ctx, cancelCtx := context.WithCancel(ctx)

	// Channel to hold errors from the goroutines
	errChan := make(chan string, len(files))

	// Concurrently process each file
	for idx, file := range files {
		wg.Add(1)
		go processFile(&wg, ctx, cancelCtx, idx, file, errChan)
	}

	// Wait until all the goroutines have finished
	wg.Wait()

	// Did an error occur with one or more files?
	select {
	case msg := <-errChan:
		fmt.Printf("Got message from error channel: %s\n", msg)
	default:
		fmt.Println("No messages on error channel")
	}

	cancelCtx()
}

func main() {

	rand.Seed(time.Now().UnixNano())

	// Generate the synthetic files
	syntheticFiles := makeSyntheticFiles(5, 1, 10, 0.8)

	// Read the files using a single-threaded approach
	singleThreadedRead(syntheticFiles)

	// Concurrent file read
	concurrentRead(syntheticFiles)
}
