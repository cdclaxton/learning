package main

import "fmt"

type Operation interface {
	Perform(int, int) int
	Equal(Operation) bool
}

type Sum struct{}

func (a Sum) Perform(x, y int) int {
	return x + y
}

func (a Sum) Equal(o Operation) bool {
	_, ok := o.(Sum)
	return ok
}

type Product struct{}

func (p Product) Perform(x, y int) int {
	return x * y
}

func (p Product) Equal(o Operation) bool {
	_, ok := o.(Product)
	return ok
}

func main() {
	ops := []Operation{
		Sum{},
		Product{},
		Sum{},
	}

	for idx := range ops {
		fmt.Printf("%d: %d\n", idx, ops[idx].Perform(4, 5))
	}

	fmt.Printf("Sum equal to Sum: %t\n", Sum{}.Equal(Sum{}))
	fmt.Printf("Product equal to Product: %t\n", Product{}.Equal(Product{}))
	fmt.Printf("Product equal to Sum: %t\n", Product{}.Equal(Sum{}))
	fmt.Printf("Sum equal to Product: %t\n", Sum{}.Equal(Product{}))
}
