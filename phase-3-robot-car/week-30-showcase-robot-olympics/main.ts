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

// Week 30 · Robot Olympics menu: A = choose event, B = start, shake = stop
let events = ["LINE", "MAZE", "PARK"]
let ev = 0
let mode = ""
input.onButtonPressed(Button.A, () => { ev = (ev + 1) % events.length; basic.showString(events[ev].charAt(0)) })
input.onButtonPressed(Button.B, () => {
    basic.showNumber(3); basic.showNumber(2); basic.showNumber(1)
    music.playTone(Note.C5, music.beat(BeatFraction.Half))
    if (events[ev] == "PARK") { drive(50, 50); basic.pause(1000); halt() }   // tune for your parking spot
    else mode = events[ev]
})
input.onGesture(Gesture.Shake, () => { mode = ""; halt() })
basic.forever(() => {
    if (mode == "LINE") {
        if (cuteBot.tracking(cuteBot.TrackingState.L_R_line)) drive(40, 40)
        else if (cuteBot.tracking(cuteBot.TrackingState.L_line_R_unline)) drive(0, 40)
        else if (cuteBot.tracking(cuteBot.TrackingState.L_unline_R_line)) drive(40, 0)
        else drive(-25, -25)
    } else if (mode == "MAZE") {
        if (distanceCm() < 15) { drive(-40, -40); basic.pause(300); drive(50, -50); basic.pause(450) }
        else drive(45, 45)
    }
    basic.pause(30)
})
basic.showString("L")
