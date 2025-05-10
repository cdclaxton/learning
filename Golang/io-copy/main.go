package main

import (
	"bytes"
	"fmt"
	"io"
	"strings"
)

func main() {

	// Using io.Copy0
	r := strings.NewReader("Hello")
	var dst bytes.Buffer
	nBytesWritten, err := io.Copy(&dst, r)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Printf("Number of bytes written: %d\n", nBytesWritten)
	fmt.Printf("Copy: %s\n", dst.String())

	// Using io.CopyN with a range of sizes of bytes
	for i := 1; i < 10; i++ {

		r = strings.NewReader("Hello")
		var dst2 bytes.Buffer
		nBytesWritten, err := io.CopyN(&dst2, r, int64(i))

		gotEOFError := false
		if err == io.EOF {
			gotEOFError = true
		} else if err != nil {
			panic(err)
		}

		fmt.Printf("Maximum number of bytes: %d, Number of bytes written: %d, Copy: %s (EOF error: %v)\n",
			i, nBytesWritten, dst2.String(), gotEOFError)
	}
}
