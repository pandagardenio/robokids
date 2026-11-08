// Week 28 · Tilt Remote — HAND side
radio.setGroup(28)
input.onButtonPressed(Button.A, () => radio.sendValue("stop", 0))
input.onButtonPressed(Button.B, () => radio.sendValue("honk", 1))
basic.forever(() => {
    // tilt forward = go, tilt left/right = turn. Drives backward? Remove the minus sign on y.
    let y = Math.constrain(-input.acceleration(Dimension.Y) / 15, -60, 60)
    let x = Math.constrain(input.acceleration(Dimension.X) / 25, -40, 40)
    radio.sendValue("y", Math.round(y))
    radio.sendValue("x", Math.round(x))
    basic.pause(100)
})
