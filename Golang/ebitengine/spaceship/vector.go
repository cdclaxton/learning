package main

import "math"

type Vector struct {
	X float64
	Y float64
}

func (v Vector) Normalise() Vector {
	scale := math.Sqrt(v.X*v.X + v.Y*v.Y)
	return Vector{
		X: v.X / scale,
		Y: v.Y / scale,
	}
}

func (v Vector) Add(v2 Vector) Vector {
	return Vector{
		X: v.X + v2.X,
		Y: v.Y + v2.Y,
	}
}

func (v Vector) Sub(v2 Vector) Vector {
	return Vector{
		X: v.X - v2.X,
		Y: v.Y - v2.Y,
	}
}

func (v Vector) Scale(s float64) Vector {
	return Vector{
		X: v.X * s,
		Y: v.Y * s,
	}
}

func (v Vector) Rotate(angle float64) Vector {
	return Vector{
		X: v.X*math.Cos(angle) - v.Y*math.Sin(angle),
		Y: v.Y*math.Cos(angle) + v.X*math.Sin(angle),
	}
}
