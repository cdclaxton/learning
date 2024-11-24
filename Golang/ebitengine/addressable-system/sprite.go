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

// CentredSprite is centred on (x,y).
type CentredSprite struct {
	sprite     *ebiten.Image
	x          float64
	y          float64
	rotation   float64
	halfWidth  float64
	halfHeight float64
}

func NewCentredSprite(sprite *ebiten.Image, x float64, y float64) *CentredSprite {

	bounds := sprite.Bounds()
	halfW := float64(bounds.Dx()) / 2
	halfH := float64(bounds.Dy()) / 2

	return &CentredSprite{
		sprite:     sprite,
		x:          x,
		y:          y,
		rotation:   0.0,
		halfWidth:  halfW,
		halfHeight: halfH,
	}
}

func (c *CentredSprite) Draw(screen *ebiten.Image) {
	op := &ebiten.DrawImageOptions{}

	// Rotate about its centre
	op.GeoM.Translate(-c.halfWidth, -c.halfHeight)
	op.GeoM.Rotate(c.rotation)

	// Translate to the required centre point
	op.GeoM.Translate(c.x, c.y)

	screen.DrawImage(c.sprite, op)
}

type TopCentredSprite struct {
	sprite  *ebiten.Image
	middleX float64
	topY    float64
	halfW   float64
}

func NewTopCentredSprite(sprite *ebiten.Image, middleX float64,
	topY float64) *TopCentredSprite {

	bounds := sprite.Bounds()
	halfW := float64(bounds.Dx()) / 2

	return &TopCentredSprite{
		sprite:  sprite,
		middleX: middleX,
		topY:    topY,
		halfW:   halfW,
	}
}

func (t *TopCentredSprite) Draw(screen *ebiten.Image) {
	op := &ebiten.DrawImageOptions{}
	op.GeoM.Translate(t.middleX-t.halfW, t.topY)

	screen.DrawImage(t.sprite, op)
}
