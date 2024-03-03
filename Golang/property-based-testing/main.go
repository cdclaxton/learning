package main

func ReverseSlice(s []int) []int {
	numElements := len(s)

	result := make([]int, numElements)
	for idx, value := range s {
		result[numElements-1-idx] = value
	}

	return result
}

type Person struct {
	Name string
	Age  int
}

func (p *Person) birthday() {
	p.Age += 1
}

func (p *Person) addYears(n int) {
	p.Age += n
}

func (p *Person) Equal(p2 *Person) bool {
	return p.Name == p2.Name && p.Age == p2.Age
}

func (p *Person) isOlderThan(p2 *Person) bool {
	return p.Age > p2.Age
}
