package main

import (
	"fmt"

	"github.com/hajimehoshi/ebiten/v2"
)

// Maximum number for slots for the smoke detectors, where the slots will be
// numbered 1 - maxSmokeDetectorSlots
const maxSmokeDetectorSlots = 4

type AlarmPanel struct {
	// Power switch
	powerSwitch *PowerSwitch

	// Break glass
	breakGlass *BreakGlass

	// Left panel LEDs
	fireLed         *Sprite
	powerFailureLed *Sprite

	// Smoke detectors
	smokeDetectors        []*SmokeDetector
	freeSmokeDetectorSlot int

	// Fire in zone LEDs
	fireInZoneLeds []*Sprite
	fireInZone5Led *Sprite // Break glass

	// Buttons
	lampTestButton   *Sprite
	soundAlarmButton *Sprite
	stopAlarmButton  *Sprite
	exitButton       *Sprite
	enterButton      *Sprite
}

func NewAlarmPanel() *AlarmPanel {

	fireInZoneLeds := make([]*Sprite, maxSmokeDetectorSlots+1)
	fireInZoneLeds[1] = NewSprite(LedOn, 158.740, 445.984)
	fireInZoneLeds[2] = NewSprite(LedOn, 200.315, 445.984)
	fireInZoneLeds[3] = NewSprite(LedOn, 241.890, 445.984)
	fireInZoneLeds[4] = NewSprite(LedOn, 283.465, 445.984)

	return &AlarmPanel{
		fireLed:               NewSprite(LedOn, 64, 365),
		powerFailureLed:       NewSprite(LedOn, 64, 390),
		smokeDetectors:        make([]*SmokeDetector, maxSmokeDetectorSlots+1),
		freeSmokeDetectorSlot: 1,
		fireInZoneLeds:        fireInZoneLeds,
		fireInZone5Led:        NewSprite(LedOn, 325.039, 445.984),
		lampTestButton:        NewSprite(ButtonPressed, 86, 480),
		soundAlarmButton:      NewSprite(ButtonPressed, 148.661, 480),
		stopAlarmButton:       NewSprite(ButtonPressed, 212, 480),
		exitButton:            NewSprite(ButtonPressed, 369.661, 457.102),
		enterButton:           NewSprite(ButtonPressed, 404.661, 457.102),
	}
}

// SetPowerSwitch that connects the alarm panel to the mains power.
func (a *AlarmPanel) SetPowerSwitch(powerSwitch *PowerSwitch) {
	a.powerSwitch = powerSwitch
}

func (a *AlarmPanel) SetBreakGlass(breakGlass *BreakGlass) {
	a.breakGlass = breakGlass
}

// AddSmokeDetector to the alarm panel in the required slot.
func (a *AlarmPanel) AddSmokeDetector(slot int, detector *SmokeDetector) {
	if slot <= 0 || slot > maxSmokeDetectorSlots {
		panic(fmt.Sprintf("Invalid smoke detector slot: %d", slot))
	}

	a.smokeDetectors[slot] = detector
}

func (a *AlarmPanel) Update() {

	for i := 1; i <= maxSmokeDetectorSlots; i++ {

	}
}

func (a *AlarmPanel) Draw(screen *ebiten.Image) {

	// Power failure LED
	if !a.powerSwitch.PowerOn() {
		a.powerFailureLed.Draw(screen)
	}

	// Direct triggering of the smoke detectors
	for i := 1; i <= maxSmokeDetectorSlots; i++ {
		if a.smokeDetectors[i] != nil && a.smokeDetectors[i].IsDirectlyTriggered() {
			a.fireInZoneLeds[i].Draw(screen)
		}
	}

	if a.breakGlass.IsBroken() {
		a.fireInZone5Led.Draw(screen)
	}
}
