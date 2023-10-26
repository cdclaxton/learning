package main

import (
	"context"
	"errors"
	"fmt"
	"testing"

	"github.com/cucumber/godog"
)

type contactsKey struct{}
type actualNumberKey struct{}
type actualNumberFoundKey struct{}

// checkContactsTableHeader checks the table of contacts in the feature file
// matches the expected configuration.
func checkContactsTableHeader(contactsTable *godog.Table) error {

	// Get the header
	header := contactsTable.Rows[0].Cells
	if len(header) != 2 {
		return fmt.Errorf("expected 2 columns, got %d", len(header))
	}

	// Check columns
	if header[0].Value != "name" {
		return fmt.Errorf("expected 'name', got %s", header[0].Value)
	}

	if header[1].Value != "phone number" {
		return fmt.Errorf("expected 'phone number', got %s", header[1].Value)
	}

	return nil
}

func thereAreContacts(ctx context.Context, contactsTable *godog.Table) (context.Context, error) {

	contacts := NewContacts()

	// Check the header of the table
	if err := checkContactsTableHeader(contactsTable); err != nil {
		return ctx, err
	}

	// Add the contacts
	for i := 1; i < len(contactsTable.Rows); i++ {
		name := contactsTable.Rows[i].Cells[0].Value
		number := contactsTable.Rows[i].Cells[1].Value
		contacts.Add(name, number)
	}

	// Return a context with a populated Contacts struct
	return context.WithValue(ctx, contactsKey{}, contacts), nil
}

func iGetTheContact(ctx context.Context, name string) (context.Context, error) {
	contacts, ok := ctx.Value(contactsKey{}).(*Contacts)
	if !ok {
		return ctx, errors.New("contacts struct not found")
	}

	actualNumber, ok := contacts.FindNumber(name)
	ctx = context.WithValue(ctx, actualNumberKey{}, actualNumber)
	return context.WithValue(ctx, actualNumberFoundKey{}, ok), nil
}

func thePhoneNumberShouldBe(ctx context.Context, expected string) (context.Context, error) {
	actualNumber, ok := ctx.Value(actualNumberKey{}).(string)
	if !ok {
		return ctx, errors.New("number not found")
	}

	if actualNumber != expected {
		return ctx, fmt.Errorf("expected %s, got %s", expected, actualNumber)
	}

	return ctx, nil
}

func iAddContact(ctx context.Context, name string, number string) (context.Context, error) {
	contacts, ok := ctx.Value(contactsKey{}).(*Contacts)
	if !ok {
		return ctx, errors.New("contacts struct not found")
	}

	contacts.Add(name, number)

	return context.WithValue(ctx, contactsKey{}, contacts), nil
}

func contactsShouldBe(ctx context.Context, contactsTable *godog.Table) (context.Context, error) {

	contacts, ok := ctx.Value(contactsKey{}).(*Contacts)
	if !ok {
		return ctx, errors.New("contacts struct not found")
	}

	// Check the header of the table
	if err := checkContactsTableHeader(contactsTable); err != nil {
		return ctx, err
	}

	actualContacts := contacts.SortedList()
	if len(actualContacts) != len(contactsTable.Rows) - 1 {
		return ctx, fmt.Errorf("expected %d rows, got %d",  
			len(contactsTable.Rows) - 1, len(actualContacts))
	}

	// Check the contacts
	for i := 1; i < len(contactsTable.Rows); i++ {
		expectedContact := SingleContact{
			name: contactsTable.Rows[i].Cells[0].Value,
			number: contactsTable.Rows[i].Cells[1].Value,
		}
		
		actualContact := actualContacts[i-1]
		if !actualContact.Equal(expectedContact) {
			return ctx, fmt.Errorf("expected %v, got %v", expectedContact, actualContact)
		}
	}

	return ctx, nil
}

func iRemoveTheContact(ctx context.Context, name string) (context.Context, error) {

	contacts, ok := ctx.Value(contactsKey{}).(*Contacts)
	if !ok {
		return ctx, errors.New("contacts struct not found")
	}

	contacts.Remove(name)

	return context.WithValue(ctx, contactsKey{}, contacts), nil
}

func InitializeContactsScenario(sc *godog.ScenarioContext) {
	sc.Step(`^there are contacts:$`, thereAreContacts)
	sc.Step(`^I get the contact ([A-Za-z]+)$`, iGetTheContact)
	sc.Step(`^the phone number should be ([A-Za-z0-9]+)$`, thePhoneNumberShouldBe)
	sc.Step(`^I add the contact ([A-Za-z]+) with number ([A-Za-z0-9]+)$`, iAddContact)
	sc.Step(`^the contacts should be:$`, contactsShouldBe)
	sc.Step(`^I remove the contact for ([A-Za-z]+)$`, iRemoveTheContact)
}

func TestContactsFeatures(t *testing.T) {
	suite := godog.TestSuite{
		ScenarioInitializer: InitializeContactsScenario,
		Options: &godog.Options{
		  Format:   "pretty",
		  Paths:    []string{"features/contacts.feature"},
		  TestingT: t,
		},
	  }
	
	  if suite.Run() != 0 {
		t.Fatal("non-zero status returned, failed to run feature tests")
	  }
}