package main

import (
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

// BreakGlass alarm trigger.
type BreakGlass struct {
	isBroken bool
	sprite   *Sprite
}

// NewBreakGlass alarm trigger.
func NewBreakGlass() *BreakGlass {
	return &BreakGlass{
		isBroken: false,
		sprite:   NewSprite(LedOn, 557.464, 536.347),
	}
}

func (b *BreakGlass) Update() {
	if ebiten.IsKeyPressed(ebiten.KeyB) && inpututil.IsKeyJustPressed(ebiten.KeyB) {
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
