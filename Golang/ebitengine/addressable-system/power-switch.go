package main

type PowerSwitch struct {
	PowerOn bool
}

func NewPowerSwitch() *PowerSwitch {
	return &PowerSwitch{
		PowerOn: true,
	}
}

// ChangeState of the power switch.
func (p *PowerSwitch) ChangeState() {
	p.PowerOn = !p.PowerOn
}
