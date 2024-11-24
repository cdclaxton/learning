package main

import (
	"math"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

type PowerSwitch struct {
	powerOn bool
	sprite  *CentredSprite
}

func NewPowerSwitch() *PowerSwitch {
	return &PowerSwitch{
		powerOn: true,
		sprite:  NewCentredSprite(Key, 560.0, 370.0),
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
	if ebiten.IsKeyPressed(ebiten.KeyP) && inpututil.IsKeyJustPressed(ebiten.KeyP) {
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
