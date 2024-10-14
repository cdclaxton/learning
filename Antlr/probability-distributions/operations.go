package main

func Add(v1, v2 int) int {
	return v1 + v2
}

func Sub(v1, v2 int) int {
	return v1 - v2
}

func Mul(v1, v2 int) int {
	return v1 * v2
}

func Div(v1, v2 int) int {
	return v1 / v2
}

func CombineDistributions(dist1, dist2 Distribution,
	fn func(v1, v2 int) int) Distribution {

	result := Distribution{}

	for value1, prob1 := range dist1 {
		for value2, prob2 := range dist2 {
			x := fn(value1, value2)
			_, ok := result[x]
			if !ok {
				result[x] = prob1 * prob2
			} else {
				result[x] += prob1 * prob2
			}
		}
	}

	return result
}
