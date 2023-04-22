package main

import "fmt"

type MyString string

type DiscreteProbDist map[int]float64

func f1(s MyString) {
	fmt.Printf("f1: %v\n", s)
}

func f2(p DiscreteProbDist) {
	fmt.Printf("f2: %v\n", p)
}

func f3(s []MyString) {
	for _, si := range s {
		fmt.Printf("f3: %v\n", si)
	}
}

func main() {
	fmt.Println("Types")

	var x MyString
	x = "Hello"
	f1(x)
	f1("Message 2")

	y := map[int]float64{
		0: 0.2,
		1: 0.3,
		2: 0.5,
	}
	f2(y)

	f3([]MyString{"A", "B"})
}
