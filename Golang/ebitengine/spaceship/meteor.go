package main

import (
	"math"

	"github.com/hajimehoshi/ebiten/v2"
	"golang.org/x/exp/rand"
)

type Meteor struct {
	sprite        Sprite
	delta         Vector  // Position change per tick
	rotationDelta float64 // Angle change per tick
}

func NewMeteor() *Meteor {
	// Select a random meteor sprite
	sprite := MeteorSprites[rand.Intn(len(MeteorSprites))]

	// Target position for the meteor to get to
	target := Vector{
		X: ScreenWidth / 2,
		Y: ScreenHeight / 2,
	}

	r := ScreenWidth / 2.0

	// Random angle in the range 0 to 2 pi
	angle := rand.Float64() * 2 * math.Pi

	// Random position on the circumference of the circle of radius r
	pos := Vector{
		X: target.X + math.Cos(angle)*r,
		Y: target.Y + math.Sin(angle)*r,
	}

	// Random speed of the meteor
	speed := 0.25 + rand.Float64()*1.5

	// Change in the meteor's position each tick
	delta := target.Sub(pos).Normalise().Scale(speed)

	// Random initial angle
	initialAngle := rand.Float64() * 2 * math.Pi

	// Random rotation speed
	maxRotation := 0.15
	rotationDelta := -(maxRotation / 2) * rand.Float64() * maxRotation

	return &Meteor{
		sprite:        *NewSprite(sprite, pos, initialAngle),
		delta:         delta,
		rotationDelta: rotationDelta,
	}
}

func (m *Meteor) Update() {

	// Move the sprite
	m.sprite.position = m.sprite.position.Add(m.delta)

	// Rotate the sprite
	m.sprite.rotation += m.rotationDelta
}

func (m *Meteor) Draw(screen *ebiten.Image) {
	m.sprite.Draw(screen)
}
