package main

import (
	"math"

	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/plotutil"
	"gonum.org/v1/plot/tools/bezier"
	"gonum.org/v1/plot/vg"
)

func radiansToDegrees(radians float64) float64 {
	return radians * 180 / math.Pi
}

func degreesToRadians(degrees float64) float64 {
	return degrees * math.Pi / 180
}

type Point struct {
	X            float64
	Y            float64
	AngleDegrees float64
}

func makeOffsetPoint(p Point, length float64) Point {
	return Point{
		X:            p.X + length*math.Cos(degreesToRadians(p.AngleDegrees)),
		Y:            p.Y + length*math.Sin(degreesToRadians(p.AngleDegrees)),
		AngleDegrees: p.AngleDegrees,
	}
}

func makeControlPoints(p1, p2 Point, length float64) []Point {
	pts := make([]Point, 4)

	pts[0] = p1
	pts[1] = makeOffsetPoint(p1, length)
	pts[2] = makeOffsetPoint(p2, -length)
	pts[3] = p2

	return pts
}

func pointsToVgPoints(points []Point) []vg.Point {
	result := make([]vg.Point, len(points))

	for i, point := range points {
		result[i].X = vg.Length(point.X)
		result[i].Y = vg.Length(point.Y)
	}

	return result
}

func curve(p1, p2 Point, length float64) plotter.XYs {
	controlPoints := pointsToVgPoints(makeControlPoints(p1, p2, length))

	c := bezier.New(controlPoints...)

	n := 10
	deltaT := 1.0 / (float64(n) - 1)
	pts := make(plotter.XYs, n)

	for i := range n {
		t := float64(i) * deltaT
		pt := c.Point(t)

		pts[i].X = pt.X.Points()
		pts[i].Y = pt.Y.Points()
	}

	return pts
}

func entryPoint(p Point, length float64) plotter.XYs {
	pts := make([]Point, 2)

	pts[0] = p
	pts[1] = makeOffsetPoint(p, length)

	plotPoints := make(plotter.XYs, 2)

	for i := range 2 {
		plotPoints[i].X = pts[i].X
		plotPoints[i].Y = pts[i].Y
	}

	return plotPoints
}

func exitPoint(p Point, length float64) plotter.XYs {
	pts := make([]Point, 2)

	pts[0] = makeOffsetPoint(p, -length)
	pts[1] = p

	plotPoints := make(plotter.XYs, 2)

	for i := range 2 {
		plotPoints[i].X = pts[i].X
		plotPoints[i].Y = pts[i].Y
	}

	return plotPoints
}

func main() {

	// Define the entry and exit points
	p1 := Point{
		X:            3,
		Y:            2,
		AngleDegrees: 10,
	}

	p2 := Point{
		X:            7,
		Y:            6,
		AngleDegrees: -45,
	}

	length := 2.0

	p := plot.New()
	p.Title.Text = "Bezier curve"
	p.X.Label.Text = "x"
	p.Y.Label.Text = "y"
	p.X.Min = 0
	p.X.Max = 10
	p.Y.Min = 0
	p.Y.Max = 10

	err := plotutil.AddLinePoints(p,
		"Entry", entryPoint(p1, length),
		"Curve", curve(p1, p2, length),
		"Exit", exitPoint(p2, length),
	)
	if err != nil {
		panic(err)
	}

	// Save the plot
	if err := p.Save(4*vg.Inch, 4*vg.Inch, "./figures/plot.png"); err != nil {
		panic(err)
	}
}
