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

// Week 35 · Guard Robot
let armed = false
let alarmDistance = 30
input.onButtonPressed(Button.A, () => { armed = true; basic.showIcon(IconNames.Target) })
input.onButtonPressed(Button.B, () => { armed = false; lights(0); basic.showIcon(IconNames.Asleep) })
basic.forever(() => {
    if (armed && distanceCm() < alarmDistance) {
        for (let i = 0; i < 6; i++) {
            lights(i % 2 == 0 ? 0xff0000 : 0x0000ff)
            music.playTone(i % 2 == 0 ? Note.A5 : Note.E5, music.beat(BeatFraction.Quarter))
        }
        basic.showString("GOTCHA")
        lights(0)
    }
    basic.pause(100)
})
basic.showIcon(IconNames.Asleep)
