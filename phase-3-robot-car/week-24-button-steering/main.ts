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

// Week 24 · Button Steering
input.onButtonPressed(Button.A, () => { basic.showArrow(ArrowNames.West); drive(0, 50) })
input.onButtonPressed(Button.B, () => { basic.showArrow(ArrowNames.East); drive(50, 0) })
input.onButtonPressed(Button.AB, () => { basic.showArrow(ArrowNames.North); drive(50, 50) })
input.onGesture(Gesture.Shake, () => { basic.showIcon(IconNames.No); halt() })
input.onLogoEvent(TouchButtonEvent.Pressed, () => { drive(60, -60); basic.pause(1200); halt() })
