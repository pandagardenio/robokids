// Week 13 · Robot Heartbeat
let wait = 500
input.onButtonPressed(Button.A, () => { wait = Math.max(100, wait - 100) })   // excited
input.onButtonPressed(Button.B, () => { wait = Math.min(1500, wait + 100) })  // sleepy
basic.forever(() => {
    basic.showIcon(IconNames.Heart)
    basic.pause(wait)
    basic.showIcon(IconNames.SmallHeart)
    basic.pause(wait)
})
