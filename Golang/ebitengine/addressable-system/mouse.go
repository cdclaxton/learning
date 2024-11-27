package main

import (
	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/inpututil"
)

type Vector struct {
	X int
	Y int
}

type Box struct {
	TopLeft     Vector
	BottomRight Vector
}

func NewBox(topLeftX int, topLeftY int, bottomRightX int, bottomRightY int) *Box {
	return &Box{
		TopLeft: Vector{
			X: topLeftX,
			Y: topLeftY,
		},
		BottomRight: Vector{
			X: bottomRightX,
			Y: bottomRightY,
		},
	}
}

// InBox returns true if the (x,y) coordinates are inside the box.
func (b *Box) InBox(x int, y int) bool {
	return x >= b.TopLeft.X && x <= b.BottomRight.X &&
		y >= b.TopLeft.Y && y <= b.BottomRight.Y
}

// MouseClickedInBox returns true if the mouse was left-clicked inside the box
// just on this frame.
func MouseClickedInBox(box *Box) bool {
	if inpututil.IsMouseButtonJustPressed(ebiten.MouseButton0) {
		x, y := ebiten.CursorPosition()
		return box.InBox(x, y)
	}

	return false
}

// MousePressedInBox returns true if the mouse is left-clicked inside the box.
func MousePressedInBox(box *Box) bool {
	if ebiten.IsMouseButtonPressed(ebiten.MouseButton0) {
		x, y := ebiten.CursorPosition()
		return box.InBox(x, y)
	}
	return false
}
