// Worker pool example

package main

import (
	"context"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

type Job struct {
	Filename      string // File to process
	NumberOfLines int    // Number of lines in the file
}

// generateJobs for numFiles files, each with a maximum number of lines of maxNumberLines.
func generateJobs(numFiles int, maxNumberLines int) []Job {
	if numFiles < 0 {
		panic(fmt.Sprintf("invalid number of files: %d\n", numFiles))
	}

	jobs := make([]Job, numFiles)

	for i := 0; i < numFiles; i++ {
		jobs[i] = Job{
			Filename:      fmt.Sprintf("file-%d.txt", i),
			NumberOfLines: rand.Intn(maxNumberLines),
		}
	}

	if len(jobs) != numFiles {
		panic("incorrect number of jobs generated")
	}

	return jobs
}

func worker(ctx context.Context, cancelCtx context.CancelFunc, idx int,
	jobsChan <-chan Job, errChan chan<- string, wg *sync.WaitGroup,
	probLineFailure float64) {

	if probLineFailure < 0.0 || probLineFailure > 1.0 {
		panic(fmt.Sprintf("invalid probability of line failure: %f\n", probLineFailure))
	}

	defer wg.Done()

	for j := range jobsChan {

		fmt.Printf("Worker %d got job processing file %s with %d lines\n", idx, j.Filename, j.NumberOfLines)

		for lineIdx := 0; lineIdx < j.NumberOfLines; lineIdx++ {

			// Check to see if the worker should be prematurely ended
			select {
			case <-ctx.Done():
				if err := ctx.Err(); err != nil {
					fmt.Printf("Worker %d, ctx error: %s\n", idx, err)
				}
				return
			default:
			}

			// Delay to simulate parsing the line
			time.Sleep(10 * time.Millisecond)

			// Random chance that a line fails to parse
			if probLineFailure > rand.Float64() {
				msg := fmt.Sprintf("ERROR: File %s has error on line %d\n", j.Filename, lineIdx)
				fmt.Printf(msg)
				errChan <- msg
				cancelCtx()
			}

			fmt.Printf("Worker %d has processed line %d / %d\n", idx, lineIdx, j.NumberOfLines-1)
		}

	}

	fmt.Printf("Worker %d finishing\n", idx)
}

func main() {

	numJobs := 5
	numWorkers := 6

	rand.Seed(time.Now().UnixNano())

	// Make a context that allows workers to detect that all jobs must cease
	ctx := context.Background()
	ctx, cancelCtx := context.WithCancel(ctx)

	// Generate the jobs to run
	jobs := generateJobs(numJobs, 20)
	fmt.Printf("Generated %d jobs\n", len(jobs))

	// Make the jobs channel for the workers
	jobsChan := make(chan Job, len(jobs))

	// Make a channel to hold errors from the goroutines. The worst case
	// situation is that every worker fails simultaneously, so a buffered
	// channel is required
	errChan := make(chan string, numWorkers)

	// Make the workers
	var wg sync.WaitGroup
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go worker(ctx, cancelCtx, i, jobsChan, errChan, &wg, 0.05)
	}

	// Fill the jobs channel
	for _, j := range jobs {
		jobsChan <- j
	}
	close(jobsChan)

	fmt.Println("Waiting for jobs to complete")
	wg.Wait()
	fmt.Println("Jobs complete")

	// Extract the first error from the error channel
	select {
	case err := <-errChan:
		fmt.Printf("Got message from error channel: %s\n", err)
	default:
		fmt.Println("No messages on error channel")
	}

	cancelCtx()
	close(errChan)
}
