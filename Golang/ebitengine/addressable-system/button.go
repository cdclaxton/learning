package main

import (
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

type Button struct {
	key         ebiten.Key // Key that is assigned to this button
	pressed     bool       // Is the key being pressed?
	justPressed bool       // Has the key been pressed in this game loop?
	sprite      *Sprite    // Button depress sprite
}

func NewButton(key ebiten.Key, sprite *Sprite) *Button {
	return &Button{
		key:         key,
		pressed:     false,
		justPressed: false,
		sprite:      sprite,
	}
}

func (b *Button) Pressed() bool {
	return b.pressed
}

func (b *Button) JustPressed() bool {
	return b.justPressed
}

func (b *Button) Update() {
	b.pressed = ebiten.IsKeyPressed(b.key)
	b.justPressed = inpututil.IsKeyJustPressed(b.key)
}

func (b *Button) Draw(screen *ebiten.Image) {
	if b.pressed {
		b.sprite.Draw(screen)
	}
}
