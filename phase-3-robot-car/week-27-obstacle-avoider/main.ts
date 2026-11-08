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

// Week 27 · Obstacle Avoider
let tooClose = 15   // cm
let running = false
input.onButtonPressed(Button.A, () => { running = true })
input.onButtonPressed(Button.B, () => { running = false; halt() })
basic.forever(() => {
    if (!running) return
    if (distanceCm() < tooClose) {
        lights(0xff0000)
        drive(-40, -40); basic.pause(400)
        drive(50, -50); basic.pause(randint(300, 700))   // random turn
    } else {
        lights(0x00ff00)
        drive(45, 45)
    }
    basic.pause(50)
})
