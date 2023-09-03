package main

import (
	"errors"
	"fmt"
	"math/rand"
)

type Card struct {
	Symbol     string // Symbol on the card
	IsFaceDown bool   // Is the card face down?
	XPos       int    // x-position
	YPos       int    // y-position
}

type Deck struct {
	Cards     []Card
	NumCardsX int
	NumCardsY int
}

// numCardsFaceDown returns the number of cards face down.
func (d *Deck) numCardsFaceDown() int {
	faceDown := 0

	for _, card := range d.Cards {
		if card.IsFaceDown {
			faceDown += 1
		}
	}

	return faceDown
}

var (
	ErrInvalidNumCardsX        = errors.New("invalid number of cards in x direction")
	ErrInvalidNumCardsY        = errors.New("invalid number of cards in y direction")
	ErrNumCardsNotDivisibleBy2 = errors.New("number of cards is not divisible by 2")
	ErrInsufficientSymbols     = errors.New("insufficient number of symbols")
)

// generateDeck of numCardsX * numCardsY randomly placed cards with symbols.
func generateDeck(numCardsX int, numCardsY int, symbols []string) (*Deck, error) {

	if numCardsX <= 0 {
		return nil, fmt.Errorf("%w: %d", ErrInvalidNumCardsX, numCardsX)
	}

	if numCardsY <= 0 {
		return nil, fmt.Errorf("%w: %d", ErrInvalidNumCardsY, numCardsY)
	}

	if (numCardsX*numCardsY)%2 != 0 {
		return nil, fmt.Errorf("%w: %d", ErrNumCardsNotDivisibleBy2, numCardsX*numCardsY)
	}

	numCards := numCardsX * numCardsY
	numPairs := numCards / 2

	if len(symbols) < numPairs {
		return nil, fmt.Errorf("%w: need %d", ErrInsufficientSymbols, numPairs)
	}

	// Build a deck
	deck := Deck{
		Cards:     make([]Card, numCardsX*numCardsY),
		NumCardsX: numCardsX,
		NumCardsY: numCardsY,
	}

	// Generate the cards
	idx := 0
	for pairIdx := 0; pairIdx < numPairs; pairIdx++ {
		for i := 0; i < 2; i++ {
			deck.Cards[idx] = Card{
				Symbol:     symbols[pairIdx],
				IsFaceDown: true,
			}
			idx += 1
		}
	}

	// Shuffle the cards
	rand.Shuffle(numCards, func(i, j int) {
		deck.Cards[i], deck.Cards[j] = deck.Cards[j], deck.Cards[i]
	})

	// Assign the x,y positions to the cards
	idx = 0
	for x := 0; x < numCardsX; x++ {
		for y := 0; y < numCardsY; y++ {
			deck.Cards[idx].XPos = x
			deck.Cards[idx].YPos = y
			idx += 1
		}
	}

	// Return the deck of cards
	return &deck, nil
}

// Game states
type State int

const (
	ReadyState       State = iota
	OneSelectedState State = iota
	TwoSelectedState State = iota
	CompleteState    State = iota
	InvalidState     State = iota
)

type GameEngine struct {
	deckOfCards   *Deck
	state         State
	card1Selected *Card
	card2Selected *Card
}

// NewGameEngine given a deck of cards.
func NewGameEngine(deck *Deck) (*GameEngine, error) {
	if deck == nil {
		return nil, ErrDeckIsNil
	}

	if len(deck.Cards) == 0 {
		return nil, ErrDeckIsEmpty
	}

	return &GameEngine{
		deckOfCards: deck,
		state:       ReadyState,
	}, nil
}

var (
	ErrDeckIsNil         = errors.New("deck is nil")
	ErrDeckIsEmpty       = errors.New("deck is empty")
	ErrCardAlreadyFaceUp = errors.New("card already face up")
	ErrGameIsComplete    = errors.New("game is complete")
	ErrCardNotFound      = errors.New("card not found")
	ErrInvalidState      = errors.New("invalid state")
)

// GetCard given the (x,y) position
func (g *GameEngine) GetCard(xPos, yPos int) (*Card, error) {
	for _, card := range g.deckOfCards.Cards {
		if card.XPos == xPos && card.YPos == yPos {
			return &card, nil
		}
	}

	return nil, ErrCardNotFound
}

func (g *GameEngine) SelectCard(xPos, yPos int) (State, error) {

	if !(g.state == ReadyState || g.state == OneSelectedState) {
		return InvalidState, ErrInvalidState
	}

	// Try to find the selected card in the deck
	var selectedCard *Card = nil
	for i := 0; i < len(g.deckOfCards.Cards); i++ {
		card := &g.deckOfCards.Cards[i]
		if card.XPos == xPos && card.YPos == yPos {
			selectedCard = card
			if !card.IsFaceDown {
				return g.state, ErrCardAlreadyFaceUp
			}
			card.IsFaceDown = false
			break
		}
	}

	// If the card couldn't be found then return
	if selectedCard == nil {
		return InvalidState, fmt.Errorf("%w: %d,%d", ErrCardNotFound, xPos, yPos)
	}

	// Move to the next state
	switch g.state {
	case ReadyState:
		g.state = OneSelectedState
		g.card1Selected = selectedCard
	case OneSelectedState:
		g.state = TwoSelectedState
		g.card2Selected = selectedCard
	default:
		return InvalidState, ErrInvalidState
	}

	return g.state, nil
}

func (g *GameEngine) GameFinished() bool {

	if g.state == TwoSelectedState {
		// Check to see if the two cards match
		match := g.card1Selected.Symbol == g.card2Selected.Symbol

		if !match {
			g.card1Selected.IsFaceDown = true
			g.card2Selected.IsFaceDown = true

			// Prepare to move to the next round
			g.card1Selected = nil
			g.card2Selected = nil

			g.state = ReadyState

			return false

		} else if match && g.deckOfCards.numCardsFaceDown() == 0 {
			// Last two cards were selected
			g.state = CompleteState
			g.card1Selected = nil
			g.card2Selected = nil
			g.state = CompleteState
			return true
		} else {
			g.card1Selected = nil
			g.card2Selected = nil
			g.state = ReadyState
			return false
		}
	}

	return false
}
