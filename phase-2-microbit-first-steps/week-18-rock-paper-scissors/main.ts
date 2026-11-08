// Week 18 · Rock, Paper, Scissors
input.onGesture(Gesture.Shake, () => {
    let pick = randint(0, 2)
    if (pick == 0) {
        basic.showIcon(IconNames.SmallSquare)       // rock
    } else if (pick == 1) {
        basic.showIcon(IconNames.Square)            // paper
    } else {
        basic.showIcon(IconNames.Scissors)          // scissors
    }
})
basic.showString("RPS")
