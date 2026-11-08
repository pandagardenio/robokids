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

// Week 43 · Gesture-Controlled Car (CAR side). Class names must match exactly.
radio.setGroup(43)
radio.onReceivedString((label) => {
    if (label == "go") { drive(45, 45); basic.showArrow(ArrowNames.North) }
    else if (label == "left") { drive(-35, 35); basic.showArrow(ArrowNames.West) }
    else if (label == "right") { drive(35, -35); basic.showArrow(ArrowNames.East) }
    else if (label == "dance") { for (let i = 0; i < 4; i++) { drive(50, -50); basic.pause(200); drive(-50, 50); basic.pause(200) } halt() }
    else { halt(); basic.showIcon(IconNames.Square) }   // stop, nothing, or unsure
})
