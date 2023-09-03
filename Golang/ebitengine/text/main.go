package main

import (
	"fmt"
	"image/color"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/examples/resources/fonts"
	"github.com/hajimehoshi/ebiten/v2/text"
	"golang.org/x/image/font"
	"golang.org/x/image/font/opentype"
)

type Game struct {
	mplusNormalFont font.Face
	counter         int
}

func NewGame() (*Game, error) {
	game := Game{
		counter: 0,
	}

	tt, err := opentype.Parse(fonts.MPlus1pRegular_ttf)
	if err != nil {
		return nil, err
	}

	const dpi = 72
	game.mplusNormalFont, err = opentype.NewFace(tt, &opentype.FaceOptions{
		Size:    10,
		DPI:     dpi,
		Hinting: font.HintingVertical,
	})
	if err != nil {
		return nil, err
	}

	return &game, nil
}

func (g *Game) Update() error {
	g.counter++
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	msg := fmt.Sprintf("TPS: %0.2f", ebiten.ActualTPS())
	text.Draw(screen, msg, g.mplusNormalFont, 1, 10, color.White)

	msg = fmt.Sprintf("Frame number: %d", g.counter)
	text.Draw(screen, msg, g.mplusNormalFont, 1, 20, color.White)
}

func (g *Game) Layout(outsideWidth int, outsideHeight int) (int, int) {
	return 320, 240
}

func main() {
	game, err := NewGame()
	if err != nil {
		log.Fatal(err)
	}

	ebiten.SetWindowSize(320, 240)
	ebiten.SetWindowTitle("Text")
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}
