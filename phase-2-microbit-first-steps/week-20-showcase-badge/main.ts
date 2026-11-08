// Week 20 · Robot Badge: put your name here
let myName = "SAM"
input.onButtonPressed(Button.A, () => basic.showString(myName))
input.onButtonPressed(Button.B, () => basic.showIcon(IconNames.Happy))
input.onGesture(Gesture.Shake, () => basic.showNumber(randint(1, 6)))
input.onLogoEvent(TouchButtonEvent.Pressed, () => {
    music.startMelody(music.builtInMelody(Melodies.PowerUp), MelodyOptions.Once)
})
basic.forever(() => {
    basic.showIcon(IconNames.Heart)
    basic.pause(800)
    basic.showIcon(IconNames.SmallHeart)
    basic.pause(800)
})
