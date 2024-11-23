package main

import (
	"embed"
	"image"
	"log"

	_ "image/png"

	"github.com/hajimehoshi/ebiten/v2"
)

const (
	ScreenWidth  = 800
	ScreenHeight = 600
)

//go:embed assets/*
var assets embed.FS

var Background = mustLoadImage("assets/alarm-panel.png")
var LedOn = mustLoadImage("assets/led-on.png")
var ButtonPressed = mustLoadImage("assets/button-pressed.png")

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

type Game struct {
	background *Sprite
	alarmPanel *AlarmPanel
}

func NewGame() *Game {
	panel := NewAlarmPanel()

	return &Game{
		background: NewSprite(Background, 0, 0),
		alarmPanel: panel,
	}
}

func (g *Game) Update() error {
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	g.background.Draw(screen)
	g.alarmPanel.fireLed.Draw(screen)
	g.alarmPanel.powerFailureLed.Draw(screen)

	g.alarmPanel.fireZone1Led.Draw(screen)
	g.alarmPanel.fireZone2Led.Draw(screen)
	g.alarmPanel.fireZone3Led.Draw(screen)
	g.alarmPanel.fireZone4Led.Draw(screen)
	g.alarmPanel.fireZone5Led.Draw(screen)

	g.alarmPanel.lampTestButton.Draw(screen)
	g.alarmPanel.soundAlarmButton.Draw(screen)
	g.alarmPanel.stopAlarmButton.Draw(screen)
	g.alarmPanel.exitButton.Draw(screen)
	g.alarmPanel.enterButton.Draw(screen)
}

func (g *Game) Layout(outsideWidth int, outsideHeight int) (int, int) {
	return ScreenWidth, ScreenHeight
}

func main() {
	game := NewGame()
	ebiten.SetWindowSize(ScreenWidth, ScreenHeight)
	ebiten.SetWindowTitle("")
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}
