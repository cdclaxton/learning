package main

import (
	"embed"
	"image"
	"log"

	_ "image/png"

	"github.com/hajimehoshi/ebiten/v2"
)

const (
	ScreenWidth  = 800
	ScreenHeight = 600
)

//go:embed assets/*
var assets embed.FS

var Background = mustLoadImage("assets/alarm-panel.png")
var LedOn = mustLoadImage("assets/led-on.png")
var ButtonPressed = mustLoadImage("assets/button-pressed.png")
var Key = mustLoadImage("assets/key.png")

var SmokeDetectorOff = mustLoadImage("assets/smoke-alarm.png")
var SmokeDetectorLedOn = mustLoadImage("assets/smoke-alarm-led-on.png")
var SmokeDetectorFlash1 = mustLoadImage("assets/smoke-alarm-flash1.png")
var SmokeDetectorFlash2 = mustLoadImage("assets/smoke-alarm-flash2.png")

func mustLoadImage(name string) *ebiten.Image {
	f, err := assets.Open(name)
	if err != nil {
		panic(err)
	}
	defer f.Close()

	img, _, err := image.Decode(f)
	if err != nil {
		panic(err)
	}

	return ebiten.NewImageFromImage(img)
}

type Game struct {
	background *Sprite
	alarmPanel *AlarmPanel

	powerSwitch *PowerSwitch
	breakGlass  *BreakGlass

	smokeAlarm1 *SmokeDetector
	smokeAlarm2 *SmokeDetector
	smokeAlarm3 *SmokeDetector
	smokeAlarm4 *SmokeDetector
}

func NewGame() *Game {

	powerSwitch := NewPowerSwitch()
	breakGlass := NewBreakGlass()
	smokeAlarm1 := NewSmokeDetector("Lounge", 100.0, 20.0, ebiten.Key1)
	smokeAlarm2 := NewSmokeDetector("Bedroom 1", 300.0, 20.0, ebiten.Key2)
	smokeAlarm3 := NewSmokeDetector("Bedroom 2", 500.0, 20.0, ebiten.Key3)
	smokeAlarm4 := NewSmokeDetector("Landing", 700.0, 20.0, ebiten.Key4)

	// Make the alarm panel
	panel := NewAlarmPanel()
	panel.SetPowerSwitch(powerSwitch)
	panel.SetBreakGlass(breakGlass)
	panel.AddSmokeDetector(1, smokeAlarm1)
	panel.AddSmokeDetector(2, smokeAlarm2)
	panel.AddSmokeDetector(3, smokeAlarm3)
	panel.AddSmokeDetector(4, smokeAlarm4)

	return &Game{
		background:  NewSprite(Background, 0, 0),
		alarmPanel:  panel,
		powerSwitch: powerSwitch,
		breakGlass:  breakGlass,
		smokeAlarm1: smokeAlarm1,
		smokeAlarm2: smokeAlarm2,
		smokeAlarm3: smokeAlarm3,
		smokeAlarm4: smokeAlarm4,
	}
}

func (g *Game) Update() error {

	// Update the power switch
	g.powerSwitch.Update()

	// Update the break glass
	g.breakGlass.Update()

	// Update each of the smoke alarms
	g.smokeAlarm1.Update()
	g.smokeAlarm2.Update()
	g.smokeAlarm3.Update()
	g.smokeAlarm4.Update()

	// Update the alarm panel
	g.alarmPanel.Update()

	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	// Draw the background image
	g.background.Draw(screen)

	// Draw the key for the power switch
	g.powerSwitch.Draw(screen)

	// Draw the break glass
	g.breakGlass.Draw(screen)

	// Draw the alarm panel
	g.alarmPanel.Draw(screen)

	// Draw the smoke alarms
	g.smokeAlarm1.Draw(screen)
	g.smokeAlarm2.Draw(screen)
	g.smokeAlarm3.Draw(screen)
	g.smokeAlarm4.Draw(screen)
}

func (g *Game) Layout(outsideWidth int, outsideHeight int) (int, int) {
	return ScreenWidth, ScreenHeight
}

func main() {
	game := NewGame()
	ebiten.SetWindowSize(ScreenWidth, ScreenHeight)
	ebiten.SetWindowTitle("Addressable Fire Alarm System")
	if err := ebiten.RunGame(game); err != nil {
		log.Fatal(err)
	}
}
