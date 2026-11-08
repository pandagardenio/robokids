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

// Week 44 · Clap and Whistle AI (CAR side; use relay.ts from week 43 on the USB micro:bit)
radio.setGroup(43)
radio.onReceivedString((label) => {
    if (label == "clap") {           // dance
        lights(0xff00ff)
        for (let i = 0; i < 4; i++) { drive(50, -50); basic.pause(250); drive(-50, 50); basic.pause(250) }
        halt(); lights(0)
    } else if (label == "whistle") { // come back
        lights(0x00ff00); drive(-45, -45); basic.pause(1000); halt(); lights(0)
    } else if (label == "snap") {    // spin
        drive(60, -60); basic.pause(1200); halt()
    }
})
basic.showIcon(IconNames.EighthNote)
