package main

import (
	"time"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
	"golang.org/x/exp/rand"
)

// Smoke detector states
const (
	SmokeDetectorNormalLedOff = iota
	SmokeDetectorNormalLedOn
	SmokeDetectorActivated1
	SmokeDetectorActivated2
)

type SmokeDetector struct {
	spriteLedOff *TopCentredSprite
	spriteLedOn  *TopCentredSprite
	spriteFlash1 *TopCentredSprite
	spriteFlash2 *TopCentredSprite

	location          string     // Room in which the smoke detector has been placed
	state             int        // State of activation
	triggerKey        ebiten.Key // Key to trigger detector
	directlyTriggered bool       // Directly triggered or flashing in sympathy?

	// The timers control how long a sprite stays on the screen before being
	// swapped in order to make the lights flash
	ledOffTimer *Timer
	ledOnTimer  *Timer
	flashTimer  *Timer

	clickBox *Box // Mouse button click detection box
}

// randomTimeInMilliseconds returns a random time in milliseconds in the range
// [min, max].
func randomTimeInMilliseconds(min int, max int) time.Duration {
	i := rand.Intn(max-min+1) + min
	return time.Duration(i) * time.Millisecond
}

func NewSmokeDetector(location string, x float64, y float64, key ebiten.Key, clickBox *Box) *SmokeDetector {

	// Add noise to the timers to simulate manufacturing tolerances
	ledOffTimer := NewTimer(randomTimeInMilliseconds(1000, 1010))
	ledOnTimer := NewTimer(randomTimeInMilliseconds(500, 510))
	flashTimer := NewTimer(randomTimeInMilliseconds(300, 310))

	return &SmokeDetector{
		location:          location,
		state:             SmokeDetectorNormalLedOff,
		spriteLedOff:      NewTopCentredSprite(SmokeDetectorOff, x, y),
		spriteLedOn:       NewTopCentredSprite(SmokeDetectorLedOn, x, y),
		spriteFlash1:      NewTopCentredSprite(SmokeDetectorFlash1, x, y),
		spriteFlash2:      NewTopCentredSprite(SmokeDetectorFlash2, x, y),
		triggerKey:        key,
		directlyTriggered: false,
		ledOffTimer:       ledOffTimer,
		ledOnTimer:        ledOnTimer,
		flashTimer:        flashTimer,
		clickBox:          clickBox,
	}
}

// Trigger the smoke detector, which will cause the light to flash.
func (s *SmokeDetector) Trigger(direct bool) {
	s.state = SmokeDetectorActivated1
	s.flashTimer.Reset()
	s.directlyTriggered = direct
}

func (s *SmokeDetector) IsTriggered() bool {
	return s.state == SmokeDetectorActivated1 || s.state == SmokeDetectorActivated2
}

// IsDirectlyTriggered returns true if the detector was directly triggered, i.e.
// due to smoke in the room.
func (s *SmokeDetector) IsDirectlyTriggered() bool {
	return s.directlyTriggered
}

// Reset the smoke detector to its unactivated state.
func (s *SmokeDetector) Reset() {
	s.state = SmokeDetectorNormalLedOff
	s.directlyTriggered = false
}

// Update the smoke detector in the game loop.
func (s *SmokeDetector) Update() {

	switch s.state {
	case SmokeDetectorNormalLedOff:
		s.ledOffTimer.Update()
		if s.ledOffTimer.IsReady() {
			s.ledOnTimer.Reset()
			s.state = SmokeDetectorNormalLedOn
		}

	case SmokeDetectorNormalLedOn:
		s.ledOnTimer.Update()
		if s.ledOnTimer.IsReady() {
			s.ledOffTimer.Reset()
			s.state = SmokeDetectorNormalLedOff
		}

	case SmokeDetectorActivated1:
		s.flashTimer.Update()
		if s.flashTimer.IsReady() {
			s.flashTimer.Reset()
			s.state = SmokeDetectorActivated2
		}

	case SmokeDetectorActivated2:
		s.flashTimer.Update()
		if s.flashTimer.IsReady() {
			s.flashTimer.Reset()
			s.state = SmokeDetectorActivated1
		}
	}

	// Detect if the smoke detector has been triggered by a key press
	if ebiten.IsKeyPressed(s.triggerKey) && inpututil.IsKeyJustPressed(s.triggerKey) {
		s.Trigger(true)
	}

	// Detect if the smoke detector has been triggered by the mouse
	if MouseClickedInBox(s.clickBox) {
		s.Trigger(true)
	}
}

// Draw the smoke detector.
func (s *SmokeDetector) Draw(screen *ebiten.Image) {

	switch s.state {
	case SmokeDetectorNormalLedOff:
		s.spriteLedOff.Draw(screen)
	case SmokeDetectorNormalLedOn:
		s.spriteLedOn.Draw(screen)
	case SmokeDetectorActivated1:
		s.spriteFlash1.Draw(screen)
	case SmokeDetectorActivated2:
		s.spriteFlash2.Draw(screen)
	}
}
