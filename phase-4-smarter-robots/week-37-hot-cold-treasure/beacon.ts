// Week 37 · Hot and Cold — BEACON (the hidden treasure)
radio.setGroup(37)
radio.setTransmitPower(7)
basic.forever(() => {
    radio.sendNumber(1)
    basic.pause(200)
})
basic.showIcon(IconNames.Diamond)
