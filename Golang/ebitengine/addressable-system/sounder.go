package main

import (
	"bytes"
	"fmt"
	"io"
	"sync/atomic"
	"time"

	"github.com/ebitengine/oto/v3"
	"github.com/hajimehoshi/go-mp3"
)

var AlarmSoundFilepath = "assets/fire-alarm.mp3"
var EnterSoundFilepath = "assets/enter.mp3"
var ExitSoundFilepath = "assets/exit.mp3"

type Sounder struct {
	otoCtx            *oto.Context
	alarmSoundDecoder *mp3.Decoder
	enterSoundDecoder *mp3.Decoder
	exitSoundDecoder  *mp3.Decoder

	ringAlarm    bool
	exitMessage  bool
	enterMessage bool

	makingSound           atomic.Bool
	shouldStopMakingSound atomic.Bool
}

func NewSounder() *Sounder {
	// Load the sounds
	alarmSound := loadSound(AlarmSoundFilepath)
	enterSound := loadSound(EnterSoundFilepath)
	exitSound := loadSound(ExitSoundFilepath)

	// Make the audio context
	otoCtx := makeAudioPlayer()

	return &Sounder{
		otoCtx:            otoCtx,
		alarmSoundDecoder: alarmSound,
		enterSoundDecoder: enterSound,
		exitSoundDecoder:  exitSound,
	}
}

func (a *Sounder) RingAlarm() {
	a.ringAlarm = true
}

func (a *Sounder) StopAlarm() {
	a.ringAlarm = false
	a.shouldStopMakingSound.Store(true)
}

func (a *Sounder) PlayExitMessage() {
	a.enterMessage = false
	a.exitMessage = true
}

func (a *Sounder) PlayEnterMessage() {
	a.enterMessage = true
	a.exitMessage = false
}

func (a *Sounder) Update() {
	if !a.makingSound.Load() {
		a.shouldStopMakingSound.Store(false)

		if a.enterMessage {
			a.playEnterSound()
		} else if a.exitMessage {
			a.playExitSound()
		} else if a.ringAlarm {
			a.playAlarm()
		}
	}
}

func (a *Sounder) playAlarm() {
	a.PlaySound(a.alarmSoundDecoder)
}

func (a *Sounder) playEnterSound() {
	a.PlaySound(a.enterSoundDecoder)
	a.enterMessage = false
}

func (a *Sounder) playExitSound() {
	a.PlaySound(a.exitSoundDecoder)
	a.exitMessage = false
}

func (a *Sounder) PlaySound(decoder *mp3.Decoder) {
	_, err := decoder.Seek(0, io.SeekStart)
	if err != nil {
		panic(err)
	}

	player := a.otoCtx.NewPlayer(decoder)
	go func(makingSound *atomic.Bool, mustStop *atomic.Bool) {

		makingSound.Store(true)
		player.Play()

		for player.IsPlaying() {
			if mustStop.Load() {
				player.Pause()
				break
			}

			time.Sleep(time.Millisecond)
		}

		err := player.Close()
		if err != nil {
			panic(err)
		}

		makingSound.Store(false)
	}(&a.makingSound, &a.shouldStopMakingSound)
}

func loadSound(filepath string) *mp3.Decoder {
	// Read the MP3 file into memory
	fileBytes, err := assets.ReadFile(filepath)
	if err != nil {
		panic(fmt.Errorf("failed to read file: %w", err))
	}

	// Convert the bytes to a reader object
	fileBytesReader := bytes.NewReader(fileBytes)

	// Decode the file
	decodedMp3, err := mp3.NewDecoder(fileBytesReader)
	if err != nil {
		panic(err)
	}

	return decodedMp3
}

func makeAudioPlayer() *oto.Context {

	op := &oto.NewContextOptions{}
	op.SampleRate = 24000
	op.ChannelCount = 2                 // 1 = mono, 2 = stereo
	op.Format = oto.FormatSignedInt16LE // Format of the source

	// Make the audio context
	otoCtx, readyChan, err := oto.NewContext(op)
	if err != nil {
		panic(err)
	}

	// Wait for the audio hardware device to be ready
	<-readyChan

	return otoCtx
}
