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

// Week 31 · Waving Robot Arm (servo on S1)
function arm(angle: number) { cuteBot.setServo(cuteBot.ServoList.S1, angle) }
let waveSpeed = 250   // smaller = more excited
input.onButtonPressed(Button.A, () => {
    basic.showIcon(IconNames.Happy)
    for (let i = 0; i < 3; i++) {
        arm(45); basic.pause(waveSpeed)
        arm(135); basic.pause(waveSpeed)
    }
    arm(90)
})
input.onButtonPressed(Button.B, () => { arm(170); basic.showString("5!") })   // high five
arm(90)
