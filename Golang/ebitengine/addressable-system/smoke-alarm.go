package main

const (
	SmokeAlarmNormalState = iota
	SmokeAlarmActivated
)

type SmokeAlarm struct {
	Location string // Room in which the smoke alarm has been placed
	State    int    // State of activation
}

func NewSmokeAlarm(location string) *SmokeAlarm {
	return &SmokeAlarm{
		Location: location,
		State:    SmokeAlarmNormalState,
	}
}

// Trigger the smoke alarm, which will cause the sounder to sound and the light
// to flash.
func (s *SmokeAlarm) Trigger() {
	s.State = SmokeAlarmActivated
}

// Reset the smoke alarm to its unactivated state.
func (s *SmokeAlarm) Reset() {
	s.State = SmokeAlarmNormalState
}
