package main

import (
	"errors"
	"fmt"
	"math/rand"
	"os"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/hints"
)

type User struct {
	ID       int `gorm:"primaryKey"`
	Username string
	Email    string
}

func (u User) String() string {
	return fmt.Sprintf("User(id=%d, Username=%s, Email=%s)", u.ID, u.Username, u.Email)
}

func connectToSqlite(t testing.TB) (*gorm.DB, error) {
	filepath := "test.db"

	// If the database already exists, then delete it for the experiment
	err := os.Remove(filepath)
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		t.Fatal(err.Error())
	}

	// Create a new Sqlite database
	db, err := gorm.Open(sqlite.Open(filepath), &gorm.Config{})
	if err != nil {
		return nil, err
	}

	// Setup the database
	assert.NoError(t, db.AutoMigrate(&User{}))

	return db, nil
}

func addUsers(t testing.TB, db *gorm.DB, num int) {
	assert.True(t, num > 0)

	// Create a random number generator
	source := rand.NewSource(time.Now().Unix())
	gen := rand.New(source)

	usernames := []string{"A", "B", "C", "D", "E", "F", "G"}
	nUsernames := len(usernames)

	emails := []string{"1", "2", "3", "4", "5", "6", "7"}
	nEmails := len(emails)

	for i := 0; i < num; i++ {
		user := User{
			Username: usernames[gen.Intn(nUsernames)],
			Email:    emails[gen.Intn(nEmails)],
		}
		assert.NoError(t, db.Create(&user).Error)
	}
}

func TestDB(t *testing.T) {
	db, err := connectToSqlite(t)
	assert.NoError(t, err)

	// Add random users
	addUsers(t, db, 1000)

	// Select users from the table
	users := []User{}
	assert.NoError(t, db.Where("username in ? AND email in ?", []string{"A", "B"}, []string{"1", "2"}).Find(&users).Error)
	assert.True(t, len(users) > 0)
}

func BenchmarkDB(b *testing.B) {
	db, err := connectToSqlite(b)
	assert.NoError(b, err)

	// Add random users
	addUsers(b, db, 1000)

	// Create the index
	query := "create index if not exists idx_user_username on users (username)"
	assert.NoError(b, db.Exec(query).Error)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		users := []User{}
		// Without hint:
		//assert.NoError(b, db.Find(&users, "username in ?", []string{"A", "B"}).Error)

		//result := db.Clauses(hints.UseIndex("idx_user_username")).Where("username in ?", []string{"A", "B"}).Find(&users)

		// result := db.Find(&users, "username in ?", []string{"A", "B"})
		// assert.NoError(b, result.Error)

		// Example from: https://gorm.io/docs/hints.html
		// Doesn't work with Sqlite
		db.Clauses(hints.UseIndex("idx_user_name")).Find(&User{})

		//assert.NoError(b, db.Clauses(hints.UseIndex("idx_user_username")).Find(&users, "username in ?", []string{"A", "B"}).Error)
		assert.True(b, len(users) > 0)
	}
}
