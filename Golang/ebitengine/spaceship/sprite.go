package main

import "github.com/hajimehoshi/ebiten/v2"

type Sprite struct {
	sprite     *ebiten.Image
	halfWidth  float64
	halfHeight float64
	position   Vector
	rotation   float64 // Angle of rotation in radians
}

func NewSprite(sprite *ebiten.Image, position Vector, rotation float64) *Sprite {

	bounds := sprite.Bounds()
	halfW := float64(bounds.Dx()) / 2
	halfH := float64(bounds.Dy()) / 2

	return &Sprite{
		sprite:     sprite,
		halfWidth:  halfW,
		halfHeight: halfH,
		position:   position,
		rotation:   rotation,
	}
}

func (s *Sprite) Draw(screen *ebiten.Image) {
	op := &ebiten.DrawImageOptions{}

	// Rotate about its centre
	op.GeoM.Translate(-s.halfWidth, -s.halfHeight)
	op.GeoM.Rotate(s.rotation)

	// Translate to the required centre point
	op.GeoM.Translate(s.position.X, s.position.Y)

	screen.DrawImage(s.sprite, op)
}

func (s *Sprite) Collider() Rect {
	bounds := s.sprite.Bounds()
	width := float64(bounds.Dx())
	height := float64(bounds.Dy())

	return Rect{
		X:      s.position.X,
		Y:      s.position.Y,
		Width:  width,
		Height: height,
	}
}
