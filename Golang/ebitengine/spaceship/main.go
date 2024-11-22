package main

import (
	"embed"
	"fmt"
	"image"
	"image/color"
	_ "image/png"
	"path/filepath"
	"time"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/text"
	"golang.org/x/image/font"
	"golang.org/x/image/font/opentype"
)

const (
	ScreenWidth  = 800
	ScreenHeight = 600
)

//go:embed assets/*
var assets embed.FS

var PlayerSprite = mustLoadImage("assets/PNG/playerShip1_blue.png")
var MeteorSprites = mustLoadImages("assets/PNG/Meteors/*.png")
var BulletSprite = mustLoadImage("assets/PNG/Lasers/laserRed12.png")

var ScoreFont = mustLoadFont("assets/Kenney Blocks.ttf")

func mustLoadImage(name string) *ebiten.Image {
	f, err := assets.Open(name)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	img, _, err := image.Decode(f)
	if err != nil {
		panic(err)
	}

	return ebiten.NewImageFromImage(img)
}

func mustLoadImages(path string) []*ebiten.Image {
	matches, err := filepath.Glob(path)
	if err != nil {
		panic(err)
	}

	images := make([]*ebiten.Image, len(matches))

	for idx, filepath := range matches {
		images[idx] = mustLoadImage(filepath)
	}

	return images
}

func mustLoadFont(path string) font.Face {
	f, err := assets.ReadFile(path)
	if err != nil {
		panic(err)
	}

	tt, err := opentype.Parse(f)
	if err != nil {
		panic(err)
	}

	face, err := opentype.NewFace(tt, &opentype.FaceOptions{
		Size:    48,
		DPI:     72,
		Hinting: font.HintingVertical,
	})
	if err != nil {
		panic(err)
	}

	return face
}

// Game holds the state.
// The Update() method changes the state and Draw() reads the state and draws
// images based on it.
type Game struct {
	player           *Player
	meteorSpawnTimer *Timer
	meteors          []*Meteor
	bullets          []*Bullet
	score            int
	audioEngine      *AudioEngine
}

func NewGame() *Game {
	return &Game{
		player:           NewPlayer(),
		meteorSpawnTimer: NewTimer(1 * time.Second),
		meteors:          []*Meteor{},
		bullets:          []*Bullet{},
		score:            0,
		audioEngine:      NewAudioEngine(),
	}
}

func (g *Game) Update() error {
	// Update the player
	g.player.Update()

	// Update the bullets
	for _, bullet := range g.bullets {
		bullet.Update()
	}

	// Spawn a new meteor if required
	g.meteorSpawnTimer.Update()
	if g.meteorSpawnTimer.IsReady() {
		g.meteorSpawnTimer.Reset()
		g.meteors = append(g.meteors, NewMeteor())
	}

	// Update the meteors
	for _, m := range g.meteors {
		m.Update()
	}

	// Check for collisions between a meteor and a bullet
	for i, m := range g.meteors {
		for j, b := range g.bullets {
			if m.sprite.Collider().Intersects(b.sprite.Collider()) {
				// A meteor has collided with a bullet
				g.meteors = append(g.meteors[:i], g.meteors[i+1:]...)
				g.bullets = append(g.bullets[:j], g.bullets[j+1:]...)
				g.score++
				g.audioEngine.PlayExplosion()
			}
		}
	}

	// Check for collisions between the player and a meteor
	for _, m := range g.meteors {
		if m.sprite.Collider().Intersects(g.player.sprite.Collider()) {
			// A meteor has collided with the player
			g.player = NewPlayer()
			g.player.SetGame(g)

			g.meteors = nil
			g.bullets = nil
			g.score = 0
		}
	}

	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	// Draw the player
	g.player.Draw(screen)

	// Draw the bullets
	for _, b := range g.bullets {
		b.Draw(screen)
	}

	// Draw each of the meteors
	for _, m := range g.meteors {
		m.Draw(screen)
	}

	// Add the score
	text.Draw(screen, fmt.Sprintf("%06d", g.score), ScoreFont, ScreenWidth/2-100, 50, color.White)
}

func (g *Game) Layout(outsideWidth int, outsideHeight int) (int, int) {
	return ScreenWidth, ScreenHeight
}

func (g *Game) AddBullet(bullet *Bullet) {
	g.bullets = append(g.bullets, bullet)
}

func main() {
	g := NewGame()
	g.player.SetGame(g)

	if err := ebiten.RunGame(g); err != nil {
		panic(err)
	}
}
