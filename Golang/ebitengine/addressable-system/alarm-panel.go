package main

type AlarmPanel struct {
	fireLed *Sprite
}

func NewAlarmPanel() *AlarmPanel {
	return &AlarmPanel{
		fireLed: NewSprite(LedOn, 17, 96),
	}
}
