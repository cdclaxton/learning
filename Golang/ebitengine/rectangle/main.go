package main

import (
	"image/color"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/examples/resources/fonts"
	"github.com/hajimehoshi/ebiten/v2/text"
	"github.com/hajimehoshi/ebiten/v2/vector"
	"golang.org/x/image/font"
	"golang.org/x/image/font/opentype"
)

type Game struct {
	screenWidth     int
	screenHeight    int
	mplusNormalFont font.Face
}

func NewGame() (*Game, error) {
	game := &Game{
		screenWidth:  640,
		screenHeight: 320,
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

	return game, nil
}

func (g *Game) Update() error {
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {

	// Draw the rectangle
	xPos := float32(50.0)
	yPos := float32(20.0)
	width := float32(30.0)
	height := float32(60.0)
	rect := ebiten.NewImage(g.screenWidth, g.screenHeight)
	vector.DrawFilledRect(rect, xPos, yPos, width, height, color.White, true)

	// Put text in the middle of the rectangle
	txt := "a-b"
	r := text.BoundString(g.mplusNormalFont, txt)
	r.Dx()
	textXPos := int(xPos+(width/2.0)) - (r.Dx() / 2)
	textYPos := int(yPos+(height/2.0)) + (r.Dy() / 2)
	text.Draw(rect, txt, g.mplusNormalFont, textXPos, textYPos, color.Black)

	screen.DrawImage(rect, nil)
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
