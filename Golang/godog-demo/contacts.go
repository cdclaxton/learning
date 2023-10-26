package main

import (
	"golang.org/x/exp/maps"
	"golang.org/x/exp/slices"
)

type Contacts struct {
	contacts map[string]string
}

func NewContacts() *Contacts {
	return &Contacts{
		contacts: map[string]string{},
	}
}

func (c *Contacts) Add(name string, number string) {
	c.contacts[name] = number
}

func (c *Contacts) Remove(name string) {
	delete(c.contacts, name)
}

func (c *Contacts) FindNumber(name string) (string, bool) {
	number, ok := c.contacts[name]
	return number, ok
}

type SingleContact struct {
	name string
	number string
}

func (s SingleContact) Equal(s2 SingleContact) bool {
	return s.name == s2.name && s.number == s2.number
}

func (c *Contacts) SortedList() ([]SingleContact) {
	names := maps.Keys(c.contacts)
	slices.Sort(names)

	result := make([]SingleContact, len(names))
	for idx, name := range names {
		result[idx] = SingleContact{
			name: name,
			number: c.contacts[name],
		}
	}

	return result
}