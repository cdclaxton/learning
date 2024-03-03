package main

// brokenAdd produces the correct answer as long as a <= 100.
func brokenAdd(a, b int) int {
	if a > 100 {
		return b
	}

	return a + b
}
