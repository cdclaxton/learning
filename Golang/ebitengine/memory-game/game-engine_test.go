package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGenerateDeck(t *testing.T) {
	testCases := []struct {
		description      string
		numCardsX        int
		numCardsY        int
		symbols          []string
		expectedNumPairs int
		errorExpected    error
	}{
		{
			description:      "invalid num cards in x direction",
			numCardsX:        0,
			numCardsY:        2,
			symbols:          []string{"a", "b", "c"},
			expectedNumPairs: 0,
			errorExpected:    ErrInvalidNumCardsX,
		},
		{
			description:      "invalid num cards in y direction",
			numCardsX:        2,
			numCardsY:        0,
			symbols:          []string{"a", "b", "c"},
			expectedNumPairs: 0,
			errorExpected:    ErrInvalidNumCardsY,
		},
		{
			description:      "invalid number of pairs",
			numCardsX:        3,
			numCardsY:        1,
			symbols:          []string{"a", "b", "c"},
			expectedNumPairs: 0,
			errorExpected:    ErrNumCardsNotDivisibleBy2,
		},
		{
			description:      "insufficient symbols",
			numCardsX:        2,
			numCardsY:        2,
			symbols:          []string{"a"},
			expectedNumPairs: 0,
			errorExpected:    ErrInsufficientSymbols,
		},
		{
			description:      "two cards",
			numCardsX:        1,
			numCardsY:        2,
			symbols:          []string{"a"},
			expectedNumPairs: 1,
			errorExpected:    nil,
		},
	}

	for _, testCase := range testCases {
		deck, err := generateDeck(testCase.numCardsX, testCase.numCardsY,
			testCase.symbols)
		assert.ErrorIs(t, err, testCase.errorExpected)

		if testCase.expectedNumPairs != 0 {
			assert.Equal(t, len(deck.Cards), testCase.expectedNumPairs*2)

			symbolsInDeck := map[string]int{}
			for _, card := range deck.Cards {
				_, found := symbolsInDeck[card.Symbol]
				if !found {
					symbolsInDeck[card.Symbol] = 1
				} else {
					symbolsInDeck[card.Symbol] += 1
				}
			}

			for _, count := range symbolsInDeck {
				assert.Equal(t, 2, count)
			}

			assert.Equal(t, testCase.expectedNumPairs*2, deck.numCardsFaceDown())
		}
	}
}

func TestGameEngineTwoCards(t *testing.T) {

	deck, err := generateDeck(2, 1, []string{"a"})
	assert.NoError(t, err)

	engine, err := NewGameEngine(deck)
	assert.NoError(t, err)
	assert.Equal(t, ReadyState, engine.state)

	// Select the first card
	newState, err := engine.SelectCard(0, 0)
	assert.NoError(t, err)
	assert.Equal(t, OneSelectedState, newState)

	finished := engine.GameFinished()
	assert.False(t, finished)

	// Try to select a card that is already selected
	newState, err = engine.SelectCard(0, 0)
	assert.ErrorIs(t, err, ErrCardAlreadyFaceUp)
	assert.Equal(t, OneSelectedState, newState)

	finished = engine.GameFinished()
	assert.False(t, finished)

	// Select the other card
	newState, err = engine.SelectCard(1, 0)
	assert.NoError(t, err)
	assert.Equal(t, TwoSelectedState, newState)

	finished = engine.GameFinished()
	assert.True(t, finished)
}

// position holds the x,y positions of a matching pair.
type position struct {
	x int
	y int
}

// matchingPositions of each card in a deck.
func matchingPositions(deck *Deck) map[string][]position {

	matching := map[string][]position{}
	for _, card := range deck.Cards {

		pos := position{
			x: card.XPos,
			y: card.YPos,
		}

		// Has the card been seen before?
		_, found := matching[card.Symbol]
		if !found {
			matching[card.Symbol] = []position{}
		}

		matching[card.Symbol] = append(matching[card.Symbol], pos)
	}

	return matching
}

func selectCardInEngine(engine *GameEngine, matches map[string][]position,
	symbol string, index int) (State, error) {

	xPos := matches[symbol][index].x
	yPos := matches[symbol][index].y
	return engine.SelectCard(xPos, yPos)
}

type engineState struct {
	state            State
	numCardsFaceDown int
}

func (e engineState) IsEqual(e2 engineState) bool {
	return e.state == e2.state &&
		e.numCardsFaceDown == e2.numCardsFaceDown
}

func (e engineState) String() string {
	return fmt.Sprintf("engineState(%d,%d)", e.state, e.numCardsFaceDown)
}

func selectCardAndCheck(t *testing.T, engine *GameEngine,
	matches map[string][]position,
	symbol string, index int,
	expectedCurrentEngineState engineState,
	expectedStateAfterCardSelected engineState,
	expectedStateAfterCheck engineState,
	expectedFinished bool) {

	// Check the engine before a card is selected
	currentState := engineState{
		state:            engine.state,
		numCardsFaceDown: engine.deckOfCards.numCardsFaceDown(),
	}
	assert.True(t, expectedCurrentEngineState.IsEqual(currentState),
		fmt.Sprintf("expected: %s, actual: %s", expectedCurrentEngineState, currentState))

	// Select a card
	_, err := selectCardInEngine(engine, matches, symbol, index)
	assert.NoError(t, err)
	stateAfterCardSelected := engineState{
		state:            engine.state,
		numCardsFaceDown: engine.deckOfCards.numCardsFaceDown(),
	}
	assert.True(t, expectedStateAfterCardSelected.IsEqual(stateAfterCardSelected),
		fmt.Sprintf("expected: %s, actual: %s", expectedStateAfterCardSelected, stateAfterCardSelected))

	// Check whether the game is finished
	finished := engine.GameFinished()
	assert.Equal(t, expectedFinished, finished)
	stateAfterCheck := engineState{
		state:            engine.state,
		numCardsFaceDown: engine.deckOfCards.numCardsFaceDown(),
	}
	assert.True(t, expectedStateAfterCheck.IsEqual(stateAfterCheck),
		fmt.Sprintf("expected: %s, actual: %s", expectedStateAfterCheck, stateAfterCheck))
}

func TestGameEngineFourCards(t *testing.T) {

	deck, err := generateDeck(2, 2, []string{"a", "b"})
	assert.NoError(t, err)

	engine, err := NewGameEngine(deck)
	assert.NoError(t, err)
	assert.Equal(t, ReadyState, engine.state)

	// Find the positions of matching cards
	matches := matchingPositions(engine.deckOfCards)
	assert.Equal(t, 4, engine.deckOfCards.numCardsFaceDown())

	// Select the 1st card of round 1
	selectCardAndCheck(t, engine, matches, "a", 0,
		engineState{ReadyState, 4},
		engineState{OneSelectedState, 3},
		engineState{OneSelectedState, 3},
		false)

	// Select the 2nd card (different to the first) of round 1
	selectCardAndCheck(t, engine, matches, "b", 0,
		engineState{OneSelectedState, 3},
		engineState{TwoSelectedState, 2},
		engineState{ReadyState, 4},
		false)

	// Select the 1st card of round 2
	selectCardAndCheck(t, engine, matches, "a", 0,
		engineState{ReadyState, 4},
		engineState{OneSelectedState, 3},
		engineState{OneSelectedState, 3},
		false)

	// Select the 2nd card of round 2
	selectCardAndCheck(t, engine, matches, "a", 1,
		engineState{OneSelectedState, 3},
		engineState{TwoSelectedState, 2},
		engineState{ReadyState, 2},
		false)

	// Select the 1st card of round 3
	selectCardAndCheck(t, engine, matches, "b", 0,
		engineState{ReadyState, 2},
		engineState{OneSelectedState, 1},
		engineState{OneSelectedState, 1},
		false)

	// Select the 2nd card of round 3
	selectCardAndCheck(t, engine, matches, "b", 1,
		engineState{OneSelectedState, 1},
		engineState{TwoSelectedState, 0},
		engineState{CompleteState, 0},
		true)
}
