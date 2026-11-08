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

// Week 47 · AI Story Robot. Press A for the next scene while you read.
// One scene = move, face, sound. Moves: F forward, B back, L spin left, R spin right, D dance, S stay
let SCENES = ["F", "L", "D", "B", "S"]
let FACES = [IconNames.Happy, IconNames.Surprised, IconNames.Heart, IconNames.Sad, IconNames.Asleep]
let scene = 0
input.onButtonPressed(Button.A, () => {
    if (scene >= SCENES.length) { basic.showString("THE END"); scene = 0; return }
    basic.showIcon(FACES[scene])
    let m = SCENES[scene]
    if (m == "F") { drive(45, 45); basic.pause(1000) }
    if (m == "B") { drive(-45, -45); basic.pause(1000) }
    if (m == "L") { drive(-50, 50); basic.pause(800) }
    if (m == "R") { drive(50, -50); basic.pause(800) }
    if (m == "D") { for (let i = 0; i < 4; i++) { drive(50, -50); basic.pause(200); drive(-50, 50); basic.pause(200) } }
    halt()
    music.playTone(Note.C5, music.beat(BeatFraction.Quarter))
    scene += 1
})
basic.showNumber(1)
