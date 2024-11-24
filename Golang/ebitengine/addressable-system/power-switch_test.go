package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPowerSwitch(t *testing.T) {
	power := NewPowerSwitch()

	assert.True(t, power.powerOn)

	power.ChangeState()
	assert.False(t, power.powerOn)

	power.ChangeState()
	assert.True(t, power.powerOn)
}
