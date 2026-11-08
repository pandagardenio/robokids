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

// Week 29 · Delivery Mission
// Write the plan from the kid's paper arrows: F = forward, L = left, R = right, D = deliver (beep)
let plan = "FFRFDLFFD"
let stepTime = 600
let turnTime = 400
input.onButtonPressed(Button.A, () => {
    for (let i = 0; i < plan.length; i++) {
        let s = plan.charAt(i)
        basic.showString(s)
        if (s == "F") { drive(50, 50); basic.pause(stepTime) }
        if (s == "L") { drive(-50, 50); basic.pause(turnTime) }
        if (s == "R") { drive(50, -50); basic.pause(turnTime) }
        if (s == "D") { halt(); lights(0xffff00); music.playTone(Note.G5, music.beat(BeatFraction.Whole)); lights(0) }
        halt(); basic.pause(150)
    }
    basic.showIcon(IconNames.Yes)
})
