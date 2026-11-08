// Week 15 · Compass Robot (first run asks you to tilt and fill the screen)
basic.forever(() => {
    let h = input.compassHeading()
    if (h < 45 || h >= 315) basic.showArrow(ArrowNames.North)
    else if (h < 135) basic.showArrow(ArrowNames.West)   // north is to your left
    else if (h < 225) basic.showArrow(ArrowNames.South)
    else basic.showArrow(ArrowNames.East)                // north is to your right
})
