package main

func CombinationProbabilities(probs []float64) ([]string, []float64) {

	N := len(probs)
	combinations := make([]string, 0, 1<<N)
	combinationProbabilities := make([]float64, 0, 1<<N)

	var generate func(int, string, float64)
	generate = func(i int, s string, p float64) {
		if i == N {
			combinations = append(combinations, s)
			combinationProbabilities = append(combinationProbabilities, p)
		} else {
			generate(i+1, s+"0", p*(1-probs[i])) // State of i(th) entry is false
			generate(i+1, s+"1", p*(probs[i]))   // State of i(th) entry is true
		}
	}

	generate(0, "", 1.0)

	return combinations, combinationProbabilities
}
