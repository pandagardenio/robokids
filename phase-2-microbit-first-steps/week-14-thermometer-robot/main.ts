// Week 14 · Thermometer Robot
input.onButtonPressed(Button.A, () => {
    let t = input.temperature()
    if (t < 15) {
        basic.showLeds(`
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            `)   // snowflake
    } else if (t > 25) {
        basic.showIcon(IconNames.Diamond) // sun
    }
    basic.showNumber(t)
    basic.showString("C")
})
