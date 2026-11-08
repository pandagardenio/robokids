// Week 48 · Talking Robot: lines starting with "say:" are spoken by ai/bridge.html
serial.setBaudRate(BaudRate.BaudRate115200)
function say(text: string) {
    serial.writeLine("say:" + text)
    basic.showIcon(IconNames.Happy)
    basic.pause(300)
    basic.showIcon(IconNames.Asleep)
}
// Kid writes the answers; you type them in:
input.onButtonPressed(Button.A, () => say("My name is Robo Bob and I am six months old."))
input.onButtonPressed(Button.B, () => say("Why did the robot go on holiday? To recharge its batteries!"))
input.onGesture(Gesture.Shake, () => say("My favorite food is micro chips."))
basic.showIcon(IconNames.Asleep)
