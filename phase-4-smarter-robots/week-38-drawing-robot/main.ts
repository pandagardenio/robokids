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

// Week 38 · Drawing Robot (tape a marker at the back center)
let turn90 = 400   // tune on your floor: time to turn 90 degrees
function shape(sides: number, sideTime: number) {
    let turnTime = Math.round(turn90 * 4 / sides)   // full circle = 4 × 90°
    for (let i = 0; i < sides; i++) {
        drive(40, 40); basic.pause(sideTime)
        drive(40, -40); basic.pause(turnTime)
    }
    halt()
}
input.onButtonPressed(Button.A, () => shape(4, 800))   // square
input.onButtonPressed(Button.B, () => shape(3, 800))   // triangle
input.onButtonPressed(Button.AB, () => {               // flower: a loop of loops
    for (let p = 0; p < 6; p++) {
        shape(4, 400)
        drive(40, -40); basic.pause(Math.round(turn90 * 4 / 6))
    }
    halt()
})
