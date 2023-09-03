package main

import (
	"image/color"
	"log"

	"github.com/hajimehoshi/ebiten/v2"
)

type Game struct{}

func (g *Game) Update() error {
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	screen.Fill(color.NRGBA{0x00, 0x40, 0x80, 0xff})
}

func (g *Game) Layout(outsideWidth int, outsideHeight int) (int, int) {
	return 320, 240
}

func main() {
	game := Game{}
	ebiten.SetWindowSize(320, 240)
	ebiten.SetWindowTitle("Screen fill")
	if err := ebiten.RunGame(&game); err != nil {
		log.Fatal(err)
	}
}
