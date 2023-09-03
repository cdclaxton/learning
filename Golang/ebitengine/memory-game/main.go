package main

import (
	"fmt"
	"image/color"
	"log"

	"github.com/hajimehoshi/ebiten/examples/resources/fonts"
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/text"
	"github.com/hajimehoshi/ebiten/v2/vector"
	"golang.org/x/image/font"
	"golang.org/x/image/font/opentype"
)

type screenLayout struct {
	numCardsX    int // Number of cards in x direction
	numCardsY    int // Number of cards in y direction
	yTop         int // y spacing from top of the screen
	yBottom      int // y spacing from the bottom of the screen
	xLeft        int // x spacing from the left of the screen
	cardHeight   int // Card height
	cardWidth    int // Card width
	yCardSpacing int // Vertical spacing between cards
	xCardSpacing int // Horizontal spacing between cards
}

// windowSize given the layout (width, height).
func (s screenLayout) windowSize() (int, int) {
	width := (s.numCardsX * s.cardWidth) + (2 * s.xLeft) + (s.numCardsX-1)*s.xCardSpacing
	height := s.yTop + s.yBottom + (s.cardHeight * s.numCardsY) + (s.numCardsY-1)*s.yCardSpacing
	return width, height
}

type Game struct {
	engine          *GameEngine
	layout          screenLayout
	mplusNormalFont font.Face
	cardFont        font.Face
	frameIdx        int
	lastClickFrame  int
}

func NewGame(engine *GameEngine, layout screenLayout) (*Game, error) {

	game := &Game{
		engine:         engine,
		layout:         layout,
		frameIdx:       0,
		lastClickFrame: 0,
	}

	// Load fonts
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
		return nil,

			err
	}

	game.cardFont, err = opentype.NewFace(tt, &opentype.FaceOptions{
		Size:    20,
		DPI:     dpi,
		Hinting: font.HintingVertical,
	})
	if err != nil {
		return nil,

			err
	}

	return game, nil
}

// Update is called every game tick.
func (g *Game) Update() error {
	return nil
}

// Draw function is called every frame.
func (g *Game) Draw(screen *ebiten.Image) {

	text.Draw(screen, fmt.Sprintf("TPS: %0.2f", ebiten.ActualTPS()), g.mplusNormalFont, 1, 10, color.White)
	text.Draw(screen, fmt.Sprintf("Frame: %d", g.frameIdx), g.mplusNormalFont, 1, 20, color.White)

	screenWidth, screenHeight := g.layout.windowSize()
	rect := ebiten.NewImage(screenWidth, screenHeight)

	// Get the mouse position
	mouseXPos, mouseYPos := ebiten.CursorPosition()
	clicked := ebiten.IsMouseButtonPressed(ebiten.MouseButtonLeft)

	text.Draw(screen, fmt.Sprintf("Clicked: %v", clicked), g.mplusNormalFont, 1, 30, color.White)

	// Draw the cards
	for col := 0; col < g.layout.numCardsX; col++ {
		for row := 0; row < g.layout.numCardsY; row++ {
			xPos := g.layout.xLeft + col*(g.layout.cardWidth+g.layout.xCardSpacing)
			yPos := g.layout.yTop + row*(g.layout.cardHeight+g.layout.yCardSpacing)

			// Get the card
			card, err := g.engine.GetCard(col, row)
			if err != nil {
				log.Fatal(err)
			}

			if g.frameIdx-g.lastClickFrame == 9 {
				g.engine.GameFinished()
			} else if clicked && (g.frameIdx-g.lastClickFrame > 10) &&
				(xPos <= mouseXPos && mouseXPos <= xPos+g.layout.cardWidth) &&
				(yPos <= mouseYPos && mouseYPos <= yPos+g.layout.cardHeight) {

				_, err := g.engine.SelectCard(col, row)
				if err != nil {
					log.Fatal(err)
				}
				g.lastClickFrame = g.frameIdx
			}

			// Get the colour of the card based on whether it's face up or down
			var cardColour color.Color
			if card.IsFaceDown {
				cardColour = color.White
			} else {
				cardColour = color.NRGBA{0xFF, 0x00, 0x00, 0xFF}
			}

			// Draw the card
			vector.DrawFilledRect(rect, float32(xPos), float32(yPos),
				float32(g.layout.cardWidth), float32(g.layout.cardHeight),
				cardColour, false)

			// Add the text if the card is face up
			if !card.IsFaceDown {
				txt := card.Symbol
				r := text.BoundString(g.cardFont, txt)
				textXPos := xPos + int(g.layout.cardWidth/2.0) - (r.Dx() / 2)
				textYPos := yPos + int(g.layout.cardHeight/2.0) + (r.Dy() / 2)
				text.Draw(rect, txt, g.cardFont, textXPos, textYPos, color.White)
			}
		}
	}

	screen.DrawImage(rect, nil)
	g.frameIdx += 1
}

// Layout takes an outside size and returns the game's logical screen size.
func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return g.layout.windowSize()
}

func main() {

	deck, err := generateDeck(4, 3, []string{"a", "b", "c", "d", "e", "f"})
	if err != nil {
		log.Fatal(err)
	}

	engine, err := NewGameEngine(deck)
	if err != nil {
		log.Fatal(err)
	}

	layout := screenLayout{
		numCardsX:    4,   // Number of cards in x direction
		numCardsY:    3,   // Number of cards in y direction
		yTop:         100, // y spacing from top of the screen
		yBottom:      10,  // y spacing from the bottom of the screen
		xLeft:        10,  // x spacing from the left of the screen
		cardHeight:   100, // Card height
		cardWidth:    80,  // Card width
		yCardSpacing: 10,  // Vertical spacing between cards
		xCardSpacing: 10,  // Horizontal spacing between cards
	}

	game, err := NewGame(engine, layout)
	if err != nil {
		log.Fatal(err)
	}

	width, height := game.layout.windowSize()
	ebiten.SetWindowSize(width, height)
	ebiten.SetWindowTitle("Memory Game")
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}
