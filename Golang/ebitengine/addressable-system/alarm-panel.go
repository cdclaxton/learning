package main

type AlarmPanel struct {

	// Left panel LEDs
	fireLed         *Sprite
	powerFailureLed *Sprite

	// Fire in zone LEDs
	fireZone1Led *Sprite
	fireZone2Led *Sprite
	fireZone3Led *Sprite
	fireZone4Led *Sprite
	fireZone5Led *Sprite
}

func NewAlarmPanel() *AlarmPanel {
	return &AlarmPanel{
		fireLed:         NewSprite(LedOn, 64, 365),
		powerFailureLed: NewSprite(LedOn, 64, 390),
		fireZone1Led:    NewSprite(LedOn, 158.740, 445.984),
		fireZone2Led:    NewSprite(LedOn, 200.315, 445.984),
		fireZone3Led:    NewSprite(LedOn, 241.890, 445.984),
		fireZone4Led:    NewSprite(LedOn, 283.465, 445.984),
		fireZone5Led:    NewSprite(LedOn, 325.039, 445.984),
	}
}
