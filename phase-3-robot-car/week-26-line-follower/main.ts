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

// Week 26 · Line Follower (black tape on a light floor)
let running = false
let speed = 35
input.onButtonPressed(Button.A, () => { running = true })
input.onButtonPressed(Button.B, () => { running = false; halt() })
basic.forever(() => {
    if (!running) return
    if (cuteBot.tracking(cuteBot.TrackingState.L_R_line)) {
        drive(speed, speed)                 // both sensors on the line: straight
    } else if (cuteBot.tracking(cuteBot.TrackingState.L_line_R_unline)) {
        drive(0, speed)                     // drifting right: turn left
    } else if (cuteBot.tracking(cuteBot.TrackingState.L_unline_R_line)) {
        drive(speed, 0)                     // drifting left: turn right
    } else {
        drive(-25, -25)                     // lost the line: back up a bit
    }
})
