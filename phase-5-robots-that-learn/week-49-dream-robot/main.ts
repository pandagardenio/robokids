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

// Week 49 · Dream Robot template: fill each slot with the kid's ideas
function onButtonA() { basic.showIcon(IconNames.Happy) /* TODO */ }
function onButtonB() { basic.showIcon(IconNames.Heart) /* TODO */ }
function onShake() { drive(60, -60); basic.pause(1000); halt() }
function onSomethingClose() { lights(0xff0000); drive(-40, -40); basic.pause(400); halt(); lights(0) }
function onLoudSound() { basic.showIcon(IconNames.Surprised) }

input.onButtonPressed(Button.A, onButtonA)
input.onButtonPressed(Button.B, onButtonB)
input.onGesture(Gesture.Shake, onShake)
input.onSound(DetectedSound.Loud, onLoudSound)
basic.forever(() => {
    if (distanceCm() < 15) onSomethingClose()
    basic.pause(100)
})
basic.showString("DREAM")
