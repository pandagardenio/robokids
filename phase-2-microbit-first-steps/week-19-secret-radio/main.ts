// Week 19 · Secret Radio Messages (flash to BOTH micro:bits)
radio.setGroup(7)   // secret channel 0-255: change it so nobody else listens
input.onButtonPressed(Button.A, () => radio.sendNumber(1))
input.onButtonPressed(Button.B, () => radio.sendNumber(2))
input.onGesture(Gesture.Shake, () => radio.sendNumber(3))
radio.onReceivedNumber((n) => {
    if (n == 1) basic.showIcon(IconNames.Heart)        // come here
    if (n == 2) basic.showIcon(IconNames.Happy)        // all good
    if (n == 3) basic.showIcon(IconNames.Skull)        // danger!
    music.playTone(Note.A5, music.beat(BeatFraction.Eighth))
})
