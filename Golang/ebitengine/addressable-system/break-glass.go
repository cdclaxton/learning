package main

import (
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

// BreakGlass alarm trigger.
type BreakGlass struct {
	isBroken bool
	sprite   *Sprite
	clickBox *Box // Mouse button click detection box
}

// NewBreakGlass alarm trigger.
func NewBreakGlass() *BreakGlass {
	return &BreakGlass{
		isBroken: false,
		sprite:   NewSprite(LedOn, 557.464, 536.347),
		clickBox: NewBox(511, 449, 619, 554),
	}
}

func (b *BreakGlass) Update() {

	// Detect if the break glass has been triggered by a key press
	if ebiten.IsKeyPressed(ebiten.KeyB) && inpututil.IsKeyJustPressed(ebiten.KeyB) {
		b.isBroken = true
	}

	// Detect if the smoke detector has been triggered by the mouse
	if MouseClickedInBox(b.clickBox) {
		b.isBroken = true
	}
}

func (b *BreakGlass) Draw(screen *ebiten.Image) {
	if b.isBroken {
		b.sprite.Draw(screen)
	}
}

// IsBroken returns true if the glass is broken.
func (b *BreakGlass) IsBroken() bool {
	return b.isBroken
}

// Reset the break glass.
func (b *BreakGlass) Reset() {
	b.isBroken = false
}
