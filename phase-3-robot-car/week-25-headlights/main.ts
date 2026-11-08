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

// Week 25 · Disco Headlights
let colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff, 0x00ffff, 0xffffff]
let i = 0
input.onButtonPressed(Button.A, () => {
    i = (i + 1) % colors.length
    lights(colors[i])
})
input.onButtonPressed(Button.B, () => {   // disco dance
    for (let k = 0; k < 8; k++) {
        lights(colors[randint(0, colors.length - 1)])
        drive(k % 2 == 0 ? 50 : -50, k % 2 == 0 ? -50 : 50)
        basic.pause(300)
    }
    halt(); lights(0)
})
