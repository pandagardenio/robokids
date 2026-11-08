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

// Week 32 · Bulldozer
let wall = 12   // cm
input.onButtonPressed(Button.A, () => {
    lights(0xffa500)
    while (distanceCm() > wall) {
        drive(60, 60)
        basic.pause(50)
    }
    halt(); music.playTone(Note.C4, music.beat(BeatFraction.Half))
    drive(-50, -50); basic.pause(800)   // back up
    halt(); lights(0)
})
