package main

import (
	"math"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

type PowerSwitch struct {
	powerOn  bool
	sprite   *CentredSprite
	clickBox *Box // Mouse button click detection box
}

func NewPowerSwitch() *PowerSwitch {
	return &PowerSwitch{
		powerOn:  true,
		sprite:   NewCentredSprite(PowerKey, 560.0, 370.0),
		clickBox: NewBox(512, 322, 610, 419),
	}
}

// ChangeState of the power switch.
func (p *PowerSwitch) ChangeState() {
	p.powerOn = !p.powerOn

	if p.powerOn {
		p.sprite.rotation = 0.0
	} else {
		p.sprite.rotation = 45 * math.Pi / 180
	}
}

// Update the power switch in the game loop.
func (p *PowerSwitch) Update() {

	// Detect if the power switch has been triggered by a key press
	if ebiten.IsKeyPressed(ebiten.KeyP) && inpututil.IsKeyJustPressed(ebiten.KeyP) {
		p.ChangeState()
	}

	// Detect if the power switch has been triggered by the mouse
	if MouseButtonJustPressedInBox(p.clickBox) {
		p.ChangeState()
	}
}

func (p *PowerSwitch) Draw(screen *ebiten.Image) {
	p.sprite.Draw(screen)
}

// PowerOn returns true if the power to the alarm panel is on.
func (p *PowerSwitch) PowerOn() bool {
	return p.powerOn
}
