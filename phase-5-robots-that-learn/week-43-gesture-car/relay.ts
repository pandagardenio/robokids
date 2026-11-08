// Week 43/44 · USB RELAY: micro:bit plugged into the laptop, forwards AI labels by radio
serial.setBaudRate(BaudRate.BaudRate115200)
radio.setGroup(43)
serial.onDataReceived(serial.delimiters(Delimiters.NewLine), () => {
    let label = serial.readUntil(serial.delimiters(Delimiters.NewLine)).trim()
    radio.sendString(label)
    basic.showString(label.charAt(0))
})
basic.showIcon(IconNames.Pitchfork)
