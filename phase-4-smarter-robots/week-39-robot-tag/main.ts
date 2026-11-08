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

// Week 39 · Robot Tag — CAR (flash tagger.ts to the handheld)
radio.setGroup(39)
let it = false
radio.onReceivedNumber((n) => {
    let s = radio.receivedPacket(RadioPacketProperty.SignalStrength)
    if (s > -55 && !it) {
        it = true
        halt(); lights(0xff0000); basic.showIcon(IconNames.Angry)
        music.startMelody(music.builtInMelody(Melodies.Wawawawaa), MelodyOptions.Once)
        basic.pause(3000)
        lights(0); it = false
    }
})
basic.forever(() => {
    if (it) return
    if (distanceCm() < 15) { drive(-40, -40); basic.pause(300); drive(50, -50); basic.pause(400) }
    else drive(randint(30, 60), randint(30, 60))   // wander
    basic.pause(300)
})
