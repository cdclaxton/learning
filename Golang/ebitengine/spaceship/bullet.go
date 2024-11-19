package main

import (
	"math"

	"github.com/hajimehoshi/ebiten/v2"
)

type Bullet struct {
	sprite *Sprite
	delta  Vector
}

func NewBullet(shipPosition Vector, shipAngle float64) *Bullet {

	bulletOffset := (float64(BulletSprite.Bounds().Dy()) / 2) +
		(float64(PlayerSprite.Bounds().Dy()) / 2) + 3.0

	bulletPosition := Vector{
		X: 0.0,
		Y: -bulletOffset,
	}.Rotate(shipAngle).Add(shipPosition)

	// Bullet speed in pixels per tick
	speed := 5.0

	delta := Vector{
		X: speed * math.Sin(shipAngle),
		Y: -speed * math.Cos(shipAngle),
	}

	return &Bullet{
		sprite: NewSprite(BulletSprite, bulletPosition, shipAngle),
		delta:  delta,
	}
}

func (b *Bullet) Update() {
	// Move the bullet
	b.sprite.position = b.sprite.position.Add(b.delta)
}

func (b *Bullet) Draw(screen *ebiten.Image) {
	b.sprite.Draw(screen)
}
