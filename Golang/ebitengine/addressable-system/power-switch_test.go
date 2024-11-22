package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPowerSwitch(t *testing.T) {
	power := NewPowerSwitch()

	assert.True(t, power.PowerOn)

	power.ChangeState()
	assert.False(t, power.PowerOn)

	power.ChangeState()
	assert.True(t, power.PowerOn)
}
