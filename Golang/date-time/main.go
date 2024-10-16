package main

import (
	"fmt"
	"log"
	"sort"
	"time"
)

// generateSamplesWithMean from the start time, n samples and a mean number
// of days per sample.
func generateSamplesWithMean(startTime time.Time, n int, meanHours float64) []time.Time {

	if n < 2 {
		log.Fatalf("insufficient samples: %d", n)
	}

	if meanHours < 0 {
		log.Fatalf("mean must be positive: %f", meanHours)
	}

	samples := make([]time.Time, n)

	return samples
}

// calculateMeanTimeDiffInHours returns the mean time difference in hours.
func calculateMeanTimeDiffInHours(samples []time.Time) float64 {

	if len(samples) < 2 {
		log.Fatal("insufficient samples to calculate mean")
	}

	// Sort the samples in ascending time order
	sort.Slice(samples, func(i, j int) bool {
		return samples[i].Before(samples[j])
	})

	// Calculate the total time difference in hours
	total := 0.0
	for i := 0; i < len(samples)-1; i++ {
		total += samples[i+1].Sub(samples[i]).Hours()
	}

	// Return the mean time difference in hours
	return total / float64(len(samples)-1)
}

func main() {

	fmt.Printf("Current time: %v\n", time.Now().Format(time.RFC3339))

	// Parse a date from its ISO-8601 string representation
	layout := "2006-01-02T15:04:05.000Z"
	str := "2014-11-12T11:45:26.371Z"
	t, err := time.Parse(layout, str)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Parsed datetime: %v\n", t)

	// Parse a date in YYYY-MM-DD format
	layout = "2006-01-02"
	t, err = time.Parse(layout, "2023-08-13")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Parsed datetime: %v\n", t)
	fmt.Printf("Year = %v, month = %v, day = %v\n", t.Year(), t.Month(), t.Day())

	// Calculate the time between two dates
	t1, _ := time.Parse(layout, "2023-08-13")
	t2, _ := time.Parse(layout, "2023-08-20")
	fmt.Printf("Number of days difference = %v\n", t2.Sub(t1).Hours()/24)
	fmt.Printf("Number of hours difference = %v\n", t2.Sub(t1).Hours())
	fmt.Printf("Number of minutes difference = %v\n", t2.Sub(t1).Minutes())
	fmt.Printf("Number of seconds difference = %v\n", t2.Sub(t1).Seconds())

	// Truncate a datetime
	tNow := time.Now()
	tTruncated := time.Date(tNow.Year(), tNow.Month(), tNow.Day(), 0, 0, 0, 0, tNow.Location())
	fmt.Printf("Truncated date: %v\n", tTruncated)

	// Change the location of a date
	dateStr := "2024-10-16T08:57:21+05:00"
	t3, err := time.Parse(time.RFC3339, dateStr)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Date string: %s\n", dateStr)
	fmt.Printf("Date in current location: %s\n", t3.In(time.Now().Location()))
}
