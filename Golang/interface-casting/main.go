package main

import "fmt"

type HyphenConcatenate interface {
	ConcatenateWithHyphen() string
}

type ColonConcatenate interface {
	ConcatenateWithColon() string
}

type SimpleStruct struct {
	a int
	b string
}

func (s SimpleStruct) ConcatenateWithHyphen() string {
	return fmt.Sprintf("%d-%s", s.a, s.b)
}

func (s SimpleStruct) ConcatenateWithColon() string {
	return fmt.Sprintf("%d:%s", s.a, s.b)
}

func show(h HyphenConcatenate) {
	fmt.Printf("show: %s\n", h.ConcatenateWithHyphen())

	// Convert from one interface to another
	c, ok := h.(ColonConcatenate)
	if !ok {
		fmt.Println("Can't typecast")
	} else {
		fmt.Printf("show: %s\n", c.ConcatenateWithColon())
	}
}

func main() {
	fmt.Println("Inteface casting example")

	s := SimpleStruct{
		a: 10,
		b: "cats",
	}

	fmt.Printf("Using the struct: %s\n", s.ConcatenateWithHyphen())
	fmt.Printf("Using the struct: %s\n", s.ConcatenateWithColon())
	show(s)
}
