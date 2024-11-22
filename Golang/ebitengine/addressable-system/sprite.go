package main

import "github.com/hajimehoshi/ebiten/v2"

type Sprite struct {
	sprite   *ebiten.Image
	topLeftX int
	topLeftY int
}

// NewSprite from an image that will be located with the top left coordinates
// at (topLeftX, topLeftY).
func NewSprite(sprite *ebiten.Image, topLeftX int, topLeftY int) *Sprite {
	return &Sprite{
		sprite:   sprite,
		topLeftX: topLeftX,
		topLeftY: topLeftY,
	}
}

func (s *Sprite) Draw(screen *ebiten.Image) {
	op := &ebiten.DrawImageOptions{}
	screen.DrawImage(s.sprite, op)
}
