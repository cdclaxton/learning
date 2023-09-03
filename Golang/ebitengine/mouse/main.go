package main

import (
	"fmt"
	"image/color"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/examples/resources/fonts"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
	"github.com/hajimehoshi/ebiten/v2/text"
	"golang.org/x/image/font"
	"golang.org/x/image/font/opentype"
)

type Game struct {
	mplusNormalFont font.Face
}

func NewGame() (*Game, error) {
	game := Game{}

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
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	msg := fmt.Sprintf("TPS: %0.2f", ebiten.ActualTPS())
	text.Draw(screen, msg, g.mplusNormalFont, 1, 10, color.White)

	// Get the mouse position
	xPos, yPos := ebiten.CursorPosition()
	msg = fmt.Sprintf("Mouse position: %d, %d", xPos, yPos)
	text.Draw(screen, msg, g.mplusNormalFont, 1, 20, color.White)

	// Get whether the left mouse button is pressed
	var mouseClicked string
	if ebiten.IsMouseButtonPressed(ebiten.MouseButtonLeft) {
		mouseClicked = "true"
	} else {
		mouseClicked = "false"
	}
	msg = fmt.Sprintf("Clicked: %s", mouseClicked)
	text.Draw(screen, msg, g.mplusNormalFont, 1, 30, color.White)

	// Get whether the left mouse is been pressed in this frame
	if inpututil.IsMouseButtonJustPressed(ebiten.MouseButtonLeft) {
		screen.Fill(color.NRGBA{0x00, 0x40, 0x80, 0xff})
	}
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
	ebiten.SetWindowTitle("")
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}
