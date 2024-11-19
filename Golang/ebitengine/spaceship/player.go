package main

import (
	"math"
	"time"

	"github.com/hajimehoshi/ebiten/v2"
)

type Player struct {
	sprite        *Sprite
	game          *Game
	shootCooldown *Timer
}

func NewPlayer() *Player {
	// The player is centered on the screen
	position := Vector{
		X: ScreenWidth / 2,
		Y: ScreenHeight / 2,
	}

	return &Player{
		sprite:        NewSprite(PlayerSprite, position, 0.0),
		shootCooldown: NewTimer(200 * time.Millisecond),
	}
}

func (p *Player) Update() {

	// Rotation speed of the player
	speed := math.Pi / float64(ebiten.TPS())

	// Update the cooldown timer
	p.shootCooldown.Update()

	if ebiten.IsKeyPressed(ebiten.KeyLeft) {
		p.sprite.rotation -= speed
	}
	if ebiten.IsKeyPressed(ebiten.KeyRight) {
		p.sprite.rotation += speed
	}
	if p.shootCooldown.IsReady() && ebiten.IsKeyPressed(ebiten.KeySpace) {
		p.shootCooldown.Reset()
		p.SpawnBullet()
		p.game.audioEngine.PlayLaser()
	}
}

func (p *Player) Draw(screen *ebiten.Image) {
	p.sprite.Draw(screen)
}

func (p *Player) SetGame(game *Game) {
	p.game = game
}

func (p *Player) SpawnBullet() {
	bullet := NewBullet(p.sprite.position, p.sprite.rotation)
	p.game.AddBullet(bullet)
}
