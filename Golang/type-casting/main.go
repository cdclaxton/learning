package main

import "fmt"

type Summable interface {
	Sum() int
}

type Simple struct {
	a int
	b int
}

func NewSimple(a int, b int) *Simple {
	return &Simple{
		a: a,
		b: b,
	}
}

func (s *Simple) String() string {
	return fmt.Sprintf("&Simple(a=%d, b=%d)", s.a, s.b)
}

func (s *Simple) Sum() int {
	return s.a + s.b
}

func (s *Simple) Multiply() int {
	return s.a * s.b
}

func main() {
	fmt.Println("Type casting (assertion) experiment")

	var i interface{} = "Hello!"
	fmt.Printf("i = %v\n", i)

	i2, ok := i.(int)
	fmt.Printf("casting to int: i2 = %v, ok = %v\n", i2, ok)

	i3, ok := i.(string)
	fmt.Printf("casting to string: i3 = %v, ok = %v\n", i3, ok)

	switch v := i.(type) {
	case int:
		fmt.Printf("i is an int = %d\n", v)
	case string:
		fmt.Printf("i is a string = %s\n", v)
	}

	var s Summable = NewSimple(1, 2)
	fmt.Printf("Sum = %d\n", s.Sum())

	s2 := s.(*Simple)
	fmt.Printf("Multiply = %d\n", s2.Multiply())
	fmt.Printf("s2 = %v\n", s2)
}
