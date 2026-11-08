// Week 45 · Toy Sorter
// Receives class labels from ai/bridge.html over USB serial (one label per line)
serial.setBaudRate(BaudRate.BaudRate115200)
serial.onDataReceived(serial.delimiters(Delimiters.NewLine), () => {
    let label = serial.readUntil(serial.delimiters(Delimiters.NewLine)).trim()
    if (label == "teddy") { basic.showIcon(IconNames.Heart); music.playTone(Note.C5, music.beat(BeatFraction.Half)) }
    else if (label == "car") { basic.showIcon(IconNames.Square); music.playTone(Note.E5, music.beat(BeatFraction.Half)) }
    else if (label == "ball") { basic.showIcon(IconNames.Target); music.playTone(Note.G5, music.beat(BeatFraction.Half)) }
    else basic.showIcon(IconNames.Confused)   // nothing or unsure
})
basic.showString("?")
