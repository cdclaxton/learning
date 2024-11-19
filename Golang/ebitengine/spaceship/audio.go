package main

import (
	"bytes"
	"io"
	"os"
	"time"

	"github.com/ebitengine/oto/v3"
	"github.com/hajimehoshi/go-mp3"
)

var ExplosionSoundFilepath = "assets/explosion-91872.mp3"
var LaserSoundFilepath = "assets/laser-45816.mp3"

type AudioEngine struct {
	otoCtx           *oto.Context
	explosionDecoder *mp3.Decoder
	laserDecoder     *mp3.Decoder
}

func NewAudioEngine() *AudioEngine {
	// Load the explosion sound
	explosionSound := loadSound(ExplosionSoundFilepath)

	// Load the laser sound
	laserSound := loadSound(LaserSoundFilepath)

	// Make the audio context
	otoCtx := makeAudioPlayer()

	return &AudioEngine{
		otoCtx:           otoCtx,
		explosionDecoder: explosionSound,
		laserDecoder:     laserSound,
	}
}

func (a *AudioEngine) PlayExplosion() {
	a.PlaySound(a.explosionDecoder)
}

func (a *AudioEngine) PlayLaser() {
	a.PlaySound(a.laserDecoder)
}

func (a *AudioEngine) PlaySound(decoder *mp3.Decoder) {
	_, err := decoder.Seek(0, io.SeekStart)
	if err != nil {
		panic(err)
	}

	player := a.otoCtx.NewPlayer(decoder)
	go func() {
		player.Play()

		for player.IsPlaying() {
			time.Sleep(time.Millisecond)
		}

		err := player.Close()
		if err != nil {
			panic(err)
		}
	}()
}

func loadSound(filepath string) *mp3.Decoder {
	// Read the MP3 file into memory
	fileBytes, err := os.ReadFile(filepath)
	if err != nil {
		panic(err)
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
	op.SampleRate = 44100
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
