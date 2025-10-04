package main

import "fmt"

type calc1 struct {
	multiplier float64
}

func (c *calc1) Calculate(value float64) float64 {
	return c.multiplier * value
}

type calc2 struct {
	offset float64
}

func (c *calc2) Calculate(value float64) float64 {
	return c.offset + value
}

type Calculator interface {
	Calculate(float64) float64
}

func doOperation(c Calculator, value float64) float64 {
	return c.Calculate(value)
}

func main() {
	c1 := calc1{
		multiplier: 10,
	}
	fmt.Printf("calc1 result: %f\n", doOperation(&c1, 100))

	c2 := calc2{
		offset: 5,
	}
	fmt.Printf("calc2 result: %f\n", doOperation(&c2, 100))

}
