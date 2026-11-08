// Week 17 · Robot Music Box (micro:bit V2 speaker)
// Kid's own tune: change these notes!
let myTune = [Note.C, Note.E, Note.G, Note.E, Note.C, Note.G]
input.onButtonPressed(Button.A, () => {
    music.startMelody(music.builtInMelody(Melodies.Birthday), MelodyOptions.Once)
})
input.onButtonPressed(Button.B, () => {
    for (let n of myTune) {
        basic.showNumber(myTune.indexOf(n) + 1)
        music.playTone(n, music.beat(BeatFraction.Half))
    }
    basic.clearScreen()
})
basic.showIcon(IconNames.EighthNote)
