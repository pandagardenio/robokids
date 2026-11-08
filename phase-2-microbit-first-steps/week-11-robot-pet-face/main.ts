// Week 11 · Robot Pet Face
input.onButtonPressed(Button.A, () => basic.showIcon(IconNames.Happy))
input.onButtonPressed(Button.B, () => basic.showIcon(IconNames.Sad))
input.onButtonPressed(Button.AB, () => basic.showIcon(IconNames.Surprised))
input.onGesture(Gesture.Shake, () => {
    basic.showIcon(IconNames.Confused)
    music.playTone(Note.C5, music.beat(BeatFraction.Quarter))
})
basic.showIcon(IconNames.Asleep)
