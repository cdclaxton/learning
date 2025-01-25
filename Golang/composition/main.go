package main

import (
	"fmt"
	"strings"
)

type Author struct {
	Forename string `json:"forename"`
	Surname  string `json:"surname"`
}

func NewAuthor(forename string, surname string) Author {
	return Author{
		Forename: forename,
		Surname:  surname,
	}
}

func (a Author) fullName() string {
	return a.Forename + " " + a.Surname
}

func (a Author) isPopulated() bool {
	return len(a.Forename) > 0 && len(a.Surname) > 0
}

func (a *Author) toUpperCase() {
	a.Forename = strings.ToUpper(a.Forename)
	a.Surname = strings.ToUpper(a.Surname)
}

type Bio struct {
	Author
	BioText string `json:"BioText"`
}

func (b Bio) toString() string {
	return b.fullName() + ": " + b.BioText
}

func NewBio(author Author, text string) Bio {
	return Bio{
		Author:  author,
		BioText: text,
	}
}

type Blog struct {
	Author
	BlogText string `json:"blogText"`
}

func NewBlog(author Author, text string) Blog {
	return Blog{
		Author:   author,
		BlogText: text,
	}
}

func (b Blog) toString() string {
	return b.fullName() + ": " + b.BlogText
}

type AuthorIsPopulated interface {
	isPopulated() bool
}

func filter[T AuthorIsPopulated](s []T) []T {
	result := []T{}

	for _, si := range s {
		if si.isPopulated() {
			result = append(result, si)
		}
	}

	return result
}

func main() {
	a := NewAuthor("David", "Harris")
	fmt.Println(a.fullName())

	bio := NewBio(a, "Born 1968 in ...")
	fmt.Println(bio.toString())

	blog := NewBlog(a, "This is my first blog ...")
	fmt.Println(blog.toString())

	// Make a slice of bios and filter it
	bios := []Bio{
		NewBio(NewAuthor("Alice", "Andrews"), "Alice's bio"),
		NewBio(NewAuthor("Bob", "Bailey"), "Bob's bio"),
		NewBio(NewAuthor("Charlie", "Chapman"), "Charlie's bio"),
		NewBio(NewAuthor("", ""), "Unknown bio"),
	}

	fmt.Println(filter(bios))

	// Make a slice of blogs and filter it
	blogs := []Blog{
		NewBlog(NewAuthor("Dave", "Dickins"), "Dave's blog"),
		NewBlog(NewAuthor("", ""), "A blog"),
	}

	fmt.Println(filter(blogs))

	// Convert the authors in the bios to upper case
	for idx, bio := range bios {
		(&bio).toUpperCase()
		bios[idx] = bio
	}
	fmt.Println(bios)

	// Convert the authors in the blogs to upper case
	for idx, blog := range blogs {
		(&blog).toUpperCase()
		blogs[idx] = blog
	}
	fmt.Println(blogs)
}
