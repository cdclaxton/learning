package main

import (
	"testing"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/stretchr/testify/assert"
)

func TestSmokeAlarm(t *testing.T) {
	alarm := NewSmokeDetector("lounge", 100, 20, ebiten.Key0, nil)
	assert.Equal(t, "lounge", alarm.location)
	assert.Equal(t, SmokeDetectorNormalLedOff, alarm.state)

	alarm.Reset()
	assert.Equal(t, SmokeDetectorNormalLedOff, alarm.state)

	alarm.Trigger(true)
	assert.Equal(t, SmokeDetectorActivated1, alarm.state)

	alarm.Reset()
	assert.Equal(t, SmokeDetectorNormalLedOff, alarm.state)
}
