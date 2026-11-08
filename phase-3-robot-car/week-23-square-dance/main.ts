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

// Week 23 · Square Dance
let sideTime = 800
let turnTime = 400   // tune until the square closes
let corners = 4      // 3 = triangle
input.onButtonPressed(Button.A, () => {
    for (let i = 0; i < corners; i++) {
        drive(50, 50); basic.pause(sideTime)
        drive(50, -50); basic.pause(turnTime)
    }
    halt()
    music.startMelody(music.builtInMelody(Melodies.BaDing), MelodyOptions.Once)
})
