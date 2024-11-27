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
	lampTestButton   *Button
	soundAlarmButton *Button
	stopAlarmButton  *Button
	exitButton       *Button
	enterButton      *Button

	// Sounder
	sounder *Sounder
}

func NewAlarmPanel() *AlarmPanel {

	fireInZoneLeds := make([]*Sprite, maxSmokeDetectorSlots+1)
	fireInZoneLeds[1] = NewSprite(LedOn, 158.740, 445.984)
	fireInZoneLeds[2] = NewSprite(LedOn, 200.315, 445.984)
	fireInZoneLeds[3] = NewSprite(LedOn, 241.890, 445.984)
	fireInZoneLeds[4] = NewSprite(LedOn, 283.465, 445.984)

	// Buttons
	lampTestButton := NewButton("Lamp test", ebiten.KeyL, NewSprite(ButtonPressed, 86, 480), NewBox(84, 480, 104, 498))
	soundAlarmButton := NewButton("Sound alarm", ebiten.KeyA, NewSprite(ButtonPressed, 148.661, 480), NewBox(148, 479, 170, 498))
	stopAlarmButton := NewButton("Stop alarm", ebiten.KeyS, NewSprite(ButtonPressed, 212, 480), NewBox(212, 480, 233, 498))
	exitButton := NewButton("Exit", ebiten.KeyX, NewSprite(ButtonPressed, 369.661, 457.102), NewBox(370, 457, 391, 474))
	enterButton := NewButton("Enter", ebiten.KeyE, NewSprite(ButtonPressed, 404.661, 457.102), NewBox(404, 457, 425, 475))

	return &AlarmPanel{
		fireLed:               NewSprite(LedOn, 64, 365),
		powerFailureLed:       NewSprite(LedOn, 64, 390),
		smokeDetectors:        make([]*SmokeDetector, maxSmokeDetectorSlots+1),
		freeSmokeDetectorSlot: 1,
		fireInZoneLeds:        fireInZoneLeds,
		fireInZone5Led:        NewSprite(LedOn, 325.039, 445.984),
		lampTestButton:        lampTestButton,
		soundAlarmButton:      soundAlarmButton,
		stopAlarmButton:       stopAlarmButton,
		exitButton:            exitButton,
		enterButton:           enterButton,
	}
}

// SetPowerSwitch that connects the alarm panel to the mains power.
func (a *AlarmPanel) SetPowerSwitch(powerSwitch *PowerSwitch) {
	a.powerSwitch = powerSwitch
}

func (a *AlarmPanel) SetBreakGlass(breakGlass *BreakGlass) {
	a.breakGlass = breakGlass
}

func (a *AlarmPanel) SetSounder(sounder *Sounder) {
	a.sounder = sounder
}

// AddSmokeDetector to the alarm panel in the required slot.
func (a *AlarmPanel) AddSmokeDetector(slot int, detector *SmokeDetector) {
	if slot <= 0 || slot > maxSmokeDetectorSlots {
		panic(fmt.Sprintf("Invalid smoke detector slot: %d", slot))
	}

	a.smokeDetectors[slot] = detector
}

// anySensorTriggered returns true if any of the smoke detectors has been
// triggered or the break glass has been broken
func (a *AlarmPanel) anySensorTriggered() bool {

	if a.breakGlass.IsBroken() {
		return true
	}

	triggered := false

	for i := 1; i <= maxSmokeDetectorSlots; i++ {
		if a.smokeDetectors[i] != nil && a.smokeDetectors[i].IsDirectlyTriggered() {
			triggered = true
			break
		}
	}

	return triggered
}

func (a *AlarmPanel) Update() {

	// Update the buttons
	a.lampTestButton.Update()
	a.soundAlarmButton.Update()
	a.stopAlarmButton.Update()
	a.exitButton.Update()
	a.enterButton.Update()

	if a.anySensorTriggered() || a.soundAlarmButton.JustPressed() {
		for i := 1; i <= maxSmokeDetectorSlots; i++ {
			if a.smokeDetectors[i] != nil && !a.smokeDetectors[i].IsTriggered() {
				a.smokeDetectors[i].Trigger(false)
			}
		}

		a.sounder.RingAlarm()
	}

	// Reset the detectors if the stop alarm button is pressed
	if a.stopAlarmButton.JustPressed() {

		// Reset the smoke alarms
		for i := 1; i <= maxSmokeDetectorSlots; i++ {
			if a.smokeDetectors[i] != nil {
				a.smokeDetectors[i].Reset()
			}
		}

		// Reset the break glass
		a.breakGlass.Reset()

		// Stop the alarm sounder
		a.sounder.StopAlarm()
	}

	if a.exitButton.JustPressed() {
		a.sounder.PlayExitMessage()
	}

	if a.enterButton.JustPressed() {
		a.sounder.PlayEnterMessage()
	}
}

func (a *AlarmPanel) Draw(screen *ebiten.Image) {

	// Fire LED
	if a.anySensorTriggered() {
		a.fireLed.Draw(screen)
	}

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

	// Detect if the break glass is broken
	if a.breakGlass.IsBroken() {
		a.fireInZone5Led.Draw(screen)
	}

	if a.lampTestButton.Pressed() {

		a.fireLed.Draw(screen)
		a.powerFailureLed.Draw(screen)

		for i := 1; i <= maxSmokeDetectorSlots; i++ {
			a.fireInZoneLeds[i].Draw(screen)
		}

		a.fireInZone5Led.Draw(screen)
	}

	// Draw the buttons
	a.lampTestButton.Draw(screen)
	a.soundAlarmButton.Draw(screen)
	a.stopAlarmButton.Draw(screen)
	a.exitButton.Draw(screen)
	a.enterButton.Draw(screen)
}
