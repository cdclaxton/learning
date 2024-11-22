package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSmokeAlarm(t *testing.T) {
	alarm := NewSmokeAlarm("lounge")
	assert.Equal(t, "lounge", alarm.Location)
	assert.Equal(t, SmokeAlarmNormalState, alarm.State)

	alarm.Reset()
	assert.Equal(t, SmokeAlarmNormalState, alarm.State)

	alarm.Trigger()
	assert.Equal(t, SmokeAlarmActivated, alarm.State)

	alarm.Reset()
	assert.Equal(t, SmokeAlarmNormalState, alarm.State)
}
