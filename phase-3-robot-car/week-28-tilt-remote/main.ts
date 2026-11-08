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

// Week 28 · Tilt Remote — CAR side (flash remote.ts to the hand micro:bit)
radio.setGroup(28)
let gas = 0
let steer = 0
radio.onReceivedValue((name, value) => {
    if (name == "x") steer = value
    if (name == "y") gas = value
    if (name == "stop") { gas = 0; steer = 0 }
    if (name == "honk") music.playTone(Note.C5, music.beat(BeatFraction.Half))
})
basic.forever(() => {
    drive(gas + steer, gas - steer)
    basic.pause(50)
})
