// Bonus · Robot Mouse — DIY version
// Kitronik Motor Driver Board (extension "kitronik-motor-driver"), 2 N20 motors,
// paper-clip whiskers on P1 (left) and P2 (right), common wire to GND.
// ---- Kit adapter ----
function motor(m: kitronik_motor_driver.Motors, speed: number) {
    if (speed == 0) kitronik_motor_driver.motorOff(m)
    else if (speed > 0) kitronik_motor_driver.motorOn(m, kitronik_motor_driver.MotorDirection.Forward, Math.min(speed, 100))
    else kitronik_motor_driver.motorOn(m, kitronik_motor_driver.MotorDirection.Reverse, Math.min(-speed, 100))
}
function drive(left: number, right: number) {
    motor(kitronik_motor_driver.Motors.Motor1, left)
    motor(kitronik_motor_driver.Motors.Motor2, right)
}
function halt() { drive(0, 0) }
function tail(angle: number) { }   // no free servo pin on this board (motors use P0, P8, P12, P16)
pins.setPull(DigitalPin.P1, PinPullMode.PullUp)
pins.setPull(DigitalPin.P2, PinPullMode.PullUp)
function whiskerLeft(): boolean { return pins.digitalReadPin(DigitalPin.P1) == 0 }   // touching = 0
function whiskerRight(): boolean { return pins.digitalReadPin(DigitalPin.P2) == 0 }

// ---- Mouse brain (same for both versions) ----
radio.setGroup(99)
input.setSoundThreshold(SoundThreshold.Loud, 160)
let hunting = false          // button B: hunt for the cheese
let lastSignal = -128
let scared = false

function squeak() {
    music.playTone(2093, music.beat(BeatFraction.Sixteenth))
    music.playTone(2637, music.beat(BeatFraction.Sixteenth))
}
function wagTail() {
    for (let i = 0; i < 4; i++) { tail(60); basic.pause(150); tail(120); basic.pause(150) }
    tail(90)
}
function bumped(left: boolean, right: boolean) {
    halt(); squeak(); basic.showIcon(IconNames.Surprised)
    drive(-50, -50); basic.pause(350)
    if (left) drive(50, -50)          // whisker on the left: turn right
    else drive(-50, 50)               // otherwise turn left
    basic.pause(randint(250, 500))
    halt()
}

input.onButtonPressed(Button.A, () => { hunting = false; basic.showIcon(IconNames.Happy); squeak() })
input.onButtonPressed(Button.B, () => { hunting = true; lastSignal = -128; basic.showIcon(IconNames.Target) })
input.onSound(DetectedSound.Loud, () => {   // a clap: run away!
    scared = true
    squeak(); basic.showIcon(IconNames.Surprised)
    drive(-80, -80); basic.pause(500)
    drive(80, -80); basic.pause(600)
    halt(); scared = false
})

// Cheese beacon: the closer, the stronger the signal
radio.onReceivedNumber((n) => {
    if (!hunting) return
    let s = radio.receivedPacket(RadioPacketProperty.SignalStrength)
    if (s > -48) {                       // found it!
        hunting = false; halt()
        basic.showIcon(IconNames.Heart); wagTail(); squeak(); squeak()
        return
    }
    if (s < lastSignal - 2) {            // getting colder: try another direction
        drive(45, -45); basic.pause(randint(200, 450))
    }
    lastSignal = s
})

basic.forever(() => {
    if (scared) return
    if (input.lightLevel() < 15) {       // dark: freeze and sleep
        halt(); basic.showIcon(IconNames.Asleep); basic.pause(300); return
    }
    let l = whiskerLeft()
    let r = whiskerRight()
    if (l || r) { bumped(l, r); return }
    if (hunting) {
        drive(40, 40); basic.pause(60)
    } else {                             // scurry, pause, sniff, scurry
        basic.showIcon(IconNames.Happy)
        let turn = randint(-20, 20)
        drive(55 + turn, 55 - turn); basic.pause(randint(200, 600))
        if (randint(0, 4) == 0) { halt(); basic.pause(randint(300, 900)) }
    }
})
basic.showIcon(IconNames.Happy)

