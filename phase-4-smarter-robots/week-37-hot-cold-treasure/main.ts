// Week 37 · Hot and Cold — SEEKER (flash beacon.ts to the hidden micro:bit)
radio.setGroup(37)
radio.onReceivedNumber((n) => {
    // signal strength is about -95 (far) to -42 (very close)
    let s = radio.receivedPacket(RadioPacketProperty.SignalStrength)
    led.plotBarGraph(s + 95, 50)
    if (s > -50) {
        basic.showIcon(IconNames.Diamond)
        music.playTone(Note.C5, music.beat(BeatFraction.Eighth))
    }
})
