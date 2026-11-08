// Week 46 · Bad Data Experiment: same program as week 45, keep score!
// Receives class labels from ai/bridge.html over USB serial (one label per line)
serial.setBaudRate(BaudRate.BaudRate115200)
let right = 0
let wrong = 0
input.onButtonPressed(Button.A, () => { right += 1; basic.showNumber(right) })   // robot guessed right
input.onButtonPressed(Button.B, () => { wrong += 1; basic.showNumber(wrong) })   // robot guessed wrong
input.onButtonPressed(Button.AB, () => { right = 0; wrong = 0; basic.showString("NEW") })
serial.onDataReceived(serial.delimiters(Delimiters.NewLine), () => {
    let label = serial.readUntil(serial.delimiters(Delimiters.NewLine)).trim()
    if (label == "teddy") basic.showIcon(IconNames.Heart)
    else if (label == "car") basic.showIcon(IconNames.Square)
    else if (label == "ball") basic.showIcon(IconNames.Target)
    else basic.showIcon(IconNames.Confused)
})
