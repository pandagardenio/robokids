// ---- Kit adapter: Elecfreaks Cutebot (add extension "cutebot") ----
// Using another car kit? Only change these three functions.
function drive(left: number, right: number) { cuteBot.motors(left, right) }
function halt() { cuteBot.stopcar() }
function lights(color: number) { cuteBot.colorLight(cuteBot.RGBLights.ALL, color) }
function distanceCm(): number {
    let d = cuteBot.ultrasonic(cuteBot.SonarUnit.Centimeters)
    return d == 0 ? 999 : d   // 0 means "no echo" = nothing in front
}
// ---------------------------------------------------------------------

// Week 36 · Robot Moods
input.setSoundThreshold(SoundThreshold.Loud, 170)
input.onGesture(Gesture.Shake, () => {          // dizzy
    basic.showIcon(IconNames.Confused); lights(0xff00ff)
    drive(60, -60); basic.pause(1200); halt()
})
input.onSound(DetectedSound.Loud, () => {       // scared
    basic.showIcon(IconNames.Surprised); lights(0xffffff)
    drive(-60, -60); basic.pause(500); halt()
})
input.onButtonPressed(Button.A, () => {         // happy dance
    basic.showIcon(IconNames.Happy); lights(0x00ff00)
    for (let i = 0; i < 4; i++) { drive(50, -50); basic.pause(250); drive(-50, 50); basic.pause(250) }
    halt()
    music.startMelody(music.builtInMelody(Melodies.Entertainer), MelodyOptions.Once)
})
basic.forever(() => {
    if (input.lightLevel() < 20) {              // sleepy in the dark
        basic.showIcon(IconNames.Asleep); lights(0x101030)
    }
    basic.pause(500)
})
