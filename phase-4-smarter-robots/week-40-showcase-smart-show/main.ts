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

// Week 40 · Smart Robot Show: A = wave, B = follow-me for 10 s, shake = dizzy, logo = guard
function arm(angle: number) { cuteBot.setServo(cuteBot.ServoList.S1, angle) }
input.onButtonPressed(Button.A, () => {
    for (let i = 0; i < 3; i++) { arm(45); basic.pause(250); arm(135); basic.pause(250) }
    arm(90)
})
input.onButtonPressed(Button.B, () => {
    let end = input.runningTime() + 10000
    while (input.runningTime() < end) {
        let d = distanceCm()
        if (d > 25 && d < 80) drive(40, 40)
        else if (d < 15) drive(-40, -40)
        else halt()
        basic.pause(60)
    }
    halt()
})
input.onGesture(Gesture.Shake, () => { basic.showIcon(IconNames.Confused); drive(60, -60); basic.pause(1200); halt() })
input.onLogoEvent(TouchButtonEvent.Pressed, () => {
    basic.showIcon(IconNames.Target)
    while (distanceCm() > 30) basic.pause(100)
    for (let i = 0; i < 6; i++) { lights(i % 2 == 0 ? 0xff0000 : 0x0000ff); basic.pause(150) }
    lights(0); basic.showString("GOTCHA")
})
basic.showIcon(IconNames.Happy)
