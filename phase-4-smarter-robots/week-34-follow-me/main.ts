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

// Week 34 · Follow-Me Robot
let target = 20   // cm. Try 40 for a shy puppy
let running = false
input.onButtonPressed(Button.A, () => { running = true })
input.onButtonPressed(Button.B, () => { running = false; halt() })
basic.forever(() => {
    if (!running) return
    let d = distanceCm()
    if (d > 80) { halt(); basic.showIcon(IconNames.Confused) }        // lost you
    else if (d > target + 5) { drive(40, 40); basic.showIcon(IconNames.Happy) }
    else if (d < target - 5) { drive(-40, -40); basic.showIcon(IconNames.Surprised) }
    else { halt(); basic.showIcon(IconNames.Heart) }
    basic.pause(60)
})
