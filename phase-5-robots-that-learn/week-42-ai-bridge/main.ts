// Week 42 · The AI Bridge
// Receives class labels from ai/bridge.html over USB serial (one label per line)
serial.setBaudRate(BaudRate.BaudRate115200)
serial.onDataReceived(serial.delimiters(Delimiters.NewLine), () => {
    let label = serial.readUntil(serial.delimiters(Delimiters.NewLine)).trim()
    if (label == "thumbsup") basic.showIcon(IconNames.Yes)
    else if (label == "thumbsdown") basic.showIcon(IconNames.No)
    else basic.clearScreen()
})
basic.showString("AI")
