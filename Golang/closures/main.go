package main

import "fmt"

func buildFunc(a int) func(int) int {
	return func(b int) int {
		return a + b
	}
}

type LinearModel struct {
	a int
	b int
}

func evalModel(model LinearModel, x int) int {
	return model.a*x + model.b
}

func buildModelRunner(model LinearModel) func(int) int {
	return func(x int) int {
		return evalModel(model, x)
	}
}

func main() {
	f1 := buildFunc(1)
	f2 := buildFunc(2)

	fmt.Printf("f1(10) = %d\n", f1(10))
	fmt.Printf("f2(10) = %d\n", f2(10))

	mr1 := buildModelRunner(LinearModel{
		a: 10,
		b: 2,
	})
	fmt.Printf("mr1(3) = %d\n", mr1(3))
}
