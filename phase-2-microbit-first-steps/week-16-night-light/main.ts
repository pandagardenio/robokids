// Week 16 · Night-Light Robot
let darkLevel = 30   // smaller = must be darker to wake up
basic.forever(() => {
    if (input.lightLevel() < darkLevel) {
        basic.showIcon(IconNames.Happy)   // awake and glowing
        led.setBrightness(255)
    } else {
        basic.showIcon(IconNames.Asleep)
        led.setBrightness(40)
    }
    basic.pause(200)
})
