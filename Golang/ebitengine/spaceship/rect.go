package main

type Rect struct {
	X      float64 // Centre
	Y      float64 // Centre
	Width  float64
	Height float64
}

func NewRect(x, y, width, height float64) Rect {
	return Rect{
		X:      x,
		Y:      y,
		Width:  width,
		Height: height,
	}
}

func (r Rect) MinX() float64 {
	return r.X - r.Width/2
}

func (r Rect) MaxX() float64 {
	return r.X + r.Width/2
}

func (r Rect) MinY() float64 {
	return r.Y - r.Height/2
}

func (r Rect) MaxY() float64 {
	return r.Y + r.Height/2
}

func (r Rect) Intersects(other Rect) bool {
	return r.MinX() <= other.MaxX() &&
		other.MinX() <= r.MaxX() &&
		r.MinY() <= other.MaxY() &&
		other.MinY() <= r.MaxY()
}
