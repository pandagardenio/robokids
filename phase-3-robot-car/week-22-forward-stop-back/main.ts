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

// Week 22 · Forward, Stop, Back
let speed = 50   // 0-100
let time = 1000  // milliseconds (1000 = 1 second). Tune this to park!
input.onButtonPressed(Button.A, () => {
    basic.showArrow(ArrowNames.North)
    drive(speed, speed); basic.pause(time); halt()
})
input.onButtonPressed(Button.B, () => {
    basic.showArrow(ArrowNames.South)
    drive(-speed, -speed); basic.pause(time); halt()
})
