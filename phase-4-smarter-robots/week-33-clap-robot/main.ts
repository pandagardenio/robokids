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

// Week 33 · Clap-Activated Robot (micro:bit V2 microphone)
let moving = false
input.setSoundThreshold(SoundThreshold.Loud, 150)   // raise if it triggers too easily
input.onSound(DetectedSound.Loud, () => {
    moving = !moving
    if (moving) { drive(45, 45); lights(0x00ff00) } else { halt(); lights(0xff0000) }
    basic.pause(400)   // ignore the echo of the same clap
})
basic.forever(() => {
    // bar graph of how loud the room is
    led.plotBarGraph(input.soundLevel(), 255)
})
