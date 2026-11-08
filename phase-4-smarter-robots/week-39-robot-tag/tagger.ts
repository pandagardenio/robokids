// Week 39 · Robot Tag — TAGGER (handheld)
radio.setGroup(39)
basic.showIcon(IconNames.Target)
basic.forever(() => {
    radio.sendNumber(1)
    basic.pause(100)
})
