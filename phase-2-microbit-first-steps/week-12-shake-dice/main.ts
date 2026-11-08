// Week 12 · Shake Dice
let sides = 6   // try 20!
input.onGesture(Gesture.Shake, () => {
    basic.clearScreen()
    basic.pause(200)
    basic.showNumber(randint(1, sides))
})
basic.showString("SHAKE")
