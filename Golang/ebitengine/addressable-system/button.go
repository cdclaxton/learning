package main

import (
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

type Button struct {
	name        string     // Button name
	key         ebiten.Key // Key that is assigned to this button
	pressed     bool       // Is the key being pressed?
	justPressed bool       // Has the key been pressed in this game loop?
	sprite      *Sprite    // Button depress sprite
	clickBox    *Box       // Mouse button click detection box
}

func NewButton(name string, key ebiten.Key, sprite *Sprite, clickBox *Box) *Button {
	return &Button{
		name:        name,
		key:         key,
		pressed:     false,
		justPressed: false,
		sprite:      sprite,
		clickBox:    clickBox,
	}
}

func (b *Button) Pressed() bool {
	return b.pressed
}

func (b *Button) JustPressed() bool {
	return b.justPressed
}

func (b *Button) Update() {

	checkKeys := true
	if MousePressedInBox(b.clickBox) {
		b.pressed = true
		checkKeys = false
	}
	if MouseClickedInBox(b.clickBox) {
		b.justPressed = true
		return
	}

	if !checkKeys {
		return
	}

	b.pressed = ebiten.IsKeyPressed(b.key)
	b.justPressed = inpututil.IsKeyJustPressed(b.key)
}

func (b *Button) Draw(screen *ebiten.Image) {
	if b.pressed {
		b.sprite.Draw(screen)
	}
}
