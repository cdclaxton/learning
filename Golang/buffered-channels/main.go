// This code explores how to use a buffered channel as a queue between
// goroutines.
//
// A generator places elements onto the queue and workers read from the channel
// an operate on the data. The number of elements to process exceeds the
// capacity of the channel, so the generator has to wait before putting more
// elements onto the queue.

package main

import (
	"context"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// generator places numJobs jobs onto the channel (which acts as a queue).
func generator(wg *sync.WaitGroup, ctx context.Context,
	cancelCtx context.CancelFunc, numJobs int, jobsChannel chan<- int,
	probFailure float64, errChan chan<- string) {

	if probFailure < 0.0 || probFailure > 1.0 {
		panic(fmt.Sprintf("invalid probability: %f\n", probFailure))
	}

	defer wg.Done()

	for i := 0; i < numJobs; i++ {

		// Check to see if the generation should be prematurely ended
		select {
		case <-ctx.Done():
			if err := ctx.Err(); err != nil {
				fmt.Printf("generator received cancel\n")
			}
			return
		default:
		}

		if rand.Float64() < probFailure {
			fmt.Printf("generator failure occurred on job %d\n", i)
			errChan <- fmt.Sprintf("generator failure on job %d", i)
			cancelCtx()
			break
		}

		fmt.Printf("generator adding job %d\n", i)
		jobsChannel <- i
	}

	fmt.Println("generator closing jobs channel")
	close(jobsChannel)
}

// worker listens to the job channel and performs the job.
func worker(idx int, wg *sync.WaitGroup, ctx context.Context,
	cancelCtx context.CancelFunc, jobsChannel <-chan int,
	probFailure float64, errChan chan<- string) {

	if probFailure < 0.0 || probFailure > 1.0 {
		panic(fmt.Sprintf("invalid probability: %f\n", probFailure))
	}

	defer wg.Done()

	for job := range jobsChannel {

		// Check to see if the job should be prematurely ended
		select {
		case <-ctx.Done():
			if err := ctx.Err(); err != nil {
				fmt.Printf(" worker %d received cancel\n", idx)
			}
			return
		default:
		}

		fmt.Printf(" worker %d - job %d - queue length %d\n", idx, job, len(jobsChannel))
		time.Sleep(100 * time.Millisecond)

		if rand.Float64() < probFailure {
			errChan <- fmt.Sprintf(" worker %d failure on job %d", idx, job)
			cancelCtx()
			break
		}
	}

	fmt.Printf(" worker %d is closing\n", idx)
}

func main() {
	fmt.Println("Buffered channels experiment")

	channelSize := 3
	numWorkers := 2
	numJobs := 10
	probFailure := 0.1

	rand.Seed(time.Now().UnixNano())

	// Buffered channel on which to place 'jobs'
	jobsChan := make(chan int, channelSize)

	var wg sync.WaitGroup
	ctx := context.Background()
	ctx, cancelCtx := context.WithCancel(ctx)

	// Channel to hold errors from the goroutines
	errChan := make(chan string, numWorkers+1)

	// Start the generator
	wg.Add(1)
	go generator(&wg, ctx, cancelCtx, numJobs, jobsChan, probFailure, errChan)

	// Start the workers
	for workerIdx := 0; workerIdx < numWorkers; workerIdx++ {
		wg.Add(1)
		go worker(workerIdx, &wg, ctx, cancelCtx, jobsChan, probFailure, errChan)
	}

	// Wait for the generator and workers to finish
	wg.Wait()
	fmt.Println("Complete")

	// Did an error occur?
	select {
	case msg := <-errChan:
		fmt.Printf("Got message from error channel: %s\n", msg)
	default:
		fmt.Println("No messages on error channel")
	}
}
