package main

import "github.com/hajimehoshi/ebiten/v2"

type Sprite struct {
	sprite   *ebiten.Image
	topLeftX float64
	topLeftY float64
}

// NewSprite from an image that will be located with the top left coordinates
// at (topLeftX, topLeftY).
func NewSprite(sprite *ebiten.Image, topLeftX float64, topLeftY float64) *Sprite {
	return &Sprite{
		sprite:   sprite,
		topLeftX: topLeftX,
		topLeftY: topLeftY,
	}
}

func (s *Sprite) Draw(screen *ebiten.Image) {
	op := &ebiten.DrawImageOptions{}
	op.GeoM.Translate(s.topLeftX, s.topLeftY)

	screen.DrawImage(s.sprite, op)
}
