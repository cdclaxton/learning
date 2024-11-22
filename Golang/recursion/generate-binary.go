package main

// BinaryStrings, e.g. for n = 2, the function will return:
// []string{"00", "01", "10", "11"}.
func BinaryStrings(n int) []string {
	if n == 0 {
		return []string{}
	}

	result := make([]string, 0, 1<<n)

	var generate func(int, string)
	generate = func(i int, s string) {
		if i == 0 {
			result = append(result, s)
		} else {
			generate(i-1, s+"0")
			generate(i-1, s+"1")
		}
	}

	generate(n, "")

	return result
}
