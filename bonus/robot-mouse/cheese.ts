// Bonus · Robot Mouse — CHEESE beacon (second micro:bit, hide it in a cardboard cheese)
radio.setGroup(99)
radio.setTransmitPower(7)
basic.showLeds(`
    . . . . #
    . . . # #
    . . # . #
    . # . . #
    # # # # #
    `)
basic.forever(() => {
    radio.sendNumber(1)
    basic.pause(150)
})
