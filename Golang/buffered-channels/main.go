// This code explores how to use a buffered channel as a queue between
// goroutines.
//
// A generator places elements onto the queue and workers read from the channel
// an operate on the data. The number of elements to process exceeds the
// capacity of the channel, so the generator has to wait before putting more
// elements onto the queue.

package main

import (
	"fmt"
	"sync"
	"time"
)

// generator places numJobs jobs onto the channel (which acts as a queue).
func generator(wg *sync.WaitGroup, numJobs int, jobsChannel chan<- int) {
	defer wg.Done()

	for i := 0; i < numJobs; i++ {
		jobsChannel <- i
	}

	fmt.Println("Closing jobs channel")
	close(jobsChannel)
}

// worker listens to the job channel and performs the job.
func worker(idx int, wg *sync.WaitGroup, jobsChannel <-chan int) {
	defer wg.Done()

	for job := range jobsChannel {
		fmt.Printf("worker %d - job %d - queue length %d\n", idx, job, len(jobsChannel))
		time.Sleep(100 * time.Millisecond)
	}

}

func main() {
	fmt.Println("Buffered channels experiment")

	channelSize := 3
	numWorkers := 2
	numJobs := 10

	// Buffered channel on which to place 'jobs'
	jobsChan := make(chan int, channelSize)

	var wg sync.WaitGroup

	// Start the generator
	wg.Add(1)
	go generator(&wg, numJobs, jobsChan)

	// Start the workers
	for workerIdx := 0; workerIdx < numWorkers; workerIdx++ {
		wg.Add(1)
		go worker(workerIdx, &wg, jobsChan)
	}

	// Wait for the generator and workers to finish
	wg.Wait()
	fmt.Println("Complete")
}
