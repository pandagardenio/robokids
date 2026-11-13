# Bonus · Robot Mouse 🐭

**Fits after week 37** · 2–3 sessions · **Skills:** touch sensors, behaviors, radio signal strength

A little mouse that scurries around, squeaks when its whiskers touch something, runs away from claps, falls asleep in the dark, and sniffs out a cheese hidden somewhere in the house.

## Pick your version

| | Cutebot mouse | DIY mouse |
| --- | --- | --- |
| Difficulty | Easy: a costume on the car you have | Medium: you build the chassis |
| Time | 1 afternoon | 2–3 weekends |
| Whiskers | Ultrasonic sensor (feels things before touching) | Real paper-clip whiskers |
| Size | ~10 cm | ~12 cm (rat-sized is easier than mouse-sized) |
| Extra cost | ~0 € | ~25 € |
| Program | [`main.ts`](main.ts) | [`diy-mouse.ts`](diy-mouse.ts) |

Both use [`cheese.ts`](cheese.ts) on a second micro:bit as the hidden cheese.

## You need

**Both versions**
- micro:bit V2 (for the squeak and clap detection)
- Second micro:bit + battery pack for the cheese
- Grey or brown felt, a paper cup or yogurt pot for the body, a pipe cleaner or string tail, felt ears, two googly eyes
- Yellow card for a cardboard cheese wedge

**Cutebot mouse:** your Cutebot. Optional: the SG90 servo from week 31 on S1 as a wagging tail.

**DIY mouse**
- [Kitronik Motor Driver Board for micro:bit](https://kitronik.co.uk/products/5620-motor-driver-board-for-the-bbc-micro-bit-v2) (or similar)
- 2 N20 micro gear motors (~100–300 RPM, 3–6 V) with 30–40 mm wheels
- 1 small ball caster
- 3×AAA battery holder with switch
- 2 large paper clips, 3 jumper wires with crocodile clips, a small piece of stiff card for the base
- Hot glue (parent)

## Build: Cutebot mouse

1. Cut a paper cup in half lengthwise and cover it in felt: that's the body.
2. Glue on ears and googly eyes at the front, above the ultrasonic sensor (its two "eyes" stay uncovered).
3. Tape the shell over the car, leaving the micro:bit screen visible as the mouse's "heart window".
4. Optional tail: tape a pipe cleaner to the servo horn on S1.
5. Load `main.ts` with the **Cutebot** extension (see [Load the programs](#load-the-programs)).

## Build: DIY mouse

1. **Base:** cut a 7 × 11 cm card base, rounded at the front. Hot glue the two motors at the back, one on each side, shafts pointing out. Push the wheels on.
2. **Balance:** glue the ball caster under the front. The mouse should sit level.
3. **Electronics:** plug the micro:bit into the motor board and glue the board on top. Wire the left motor to Motor 1 and the right motor to Motor 2. Battery pack under or behind the board.
4. **Whiskers:** bend each paper clip into a long, springy whisker and fix one to each front corner. Connect the left whisker to **P1**, the right to **P2**. Run a bare GND wire across the front, just behind both whiskers, so a bent whisker touches it. (Check your board's labels for where P1, P2 and GND are broken out; crocodile clips on the micro:bit's edge pads also work.)
5. **Test before decorating:** load `diy-mouse.ts` with the **Kitronik Motor Driver** extension (see [Load the programs](#load-the-programs)). If the mouse spins instead of driving forward, swap one motor's two wires.
6. **Costume:** felt body over the top, ears, eyes, tail. Keep the whiskers free to move.

## Cheese

Load `cheese.ts` onto the second micro:bit and hide it inside the cardboard cheese wedge.

## Load the programs

Each program goes on a different micro:bit. Load them one at a time, with that micro:bit plugged in.

| Program | Goes on | Extension |
| --- | --- | --- |
| [`main.ts`](main.ts) | the Cutebot mouse | Cutebot |
| [`diy-mouse.ts`](diy-mouse.ts) | the DIY mouse | Kitronik Motor Driver |
| [`cheese.ts`](cheese.ts) | the hidden cheese | none |

1. Click the program link, then the **Copy raw file** button (two small squares, top right of the program).
2. Go to [makecode.microbit.org](https://makecode.microbit.org), click **New Project** and name it (for example `Mouse` or `Cheese`).
3. Mouse only: click **Extensions** at the bottom of the block list, search for the extension in the table (`cutebot` or `kitronik motor driver`) and click it.
4. Click **JavaScript** at the top, select all the text (**Ctrl+A**, Mac: **Cmd+A**) and paste (**Ctrl+V**, Mac: **Cmd+V**).
5. Click **Blocks** to see the colorful version your kid can change, then click **Download**.

First time, or something went wrong? See [Start here](../../START-HERE.md#load-a-program).

## Play

| Do this | The mouse... |
| --- | --- |
| Leave it alone | Scurries, stops to sniff, scurries again |
| Whisker touches a wall | Squeaks, backs up and turns away |
| Clap loudly | Runs away and spins |
| Turn off the lights | Freezes and falls asleep |
| Press B | Hunts for the cheese. When it finds it: heart, tail wag, double squeak |
| Press A | Stops hunting and goes back to wandering |

**Games:** hide the cheese in a cardboard maze and time the hunt. Play "cat": your kid claps when the mouse gets too close to the cat's corner. Build a mouse hole from a shoebox and see if it finds its way home.

## Talk about it

> How does the mouse know it touched something? How do real mice do it?

Real mice use their whiskers to feel their way in the dark, just like this robot.

## Level up

- Make the mouse squeak louder (more notes) the closer it gets to the cheese.
- Add a "hungry" counter that grows over time: the hungrier it is, the faster it scurries.
- Build a second mouse and have them chase each other by radio, like week 39.
- Parent challenge: turn it into a wall-following maze mouse, the first step towards [Micromouse](https://en.wikipedia.org/wiki/Micromouse).

## Tuning knobs

- `whiskerCm` (Cutebot): how close something must be before the mouse "feels" it.
- `SoundThreshold.Loud, 160`: raise it if the mouse runs away from normal talking.
- `s > -48`: how close counts as "found the cheese". Lower it (e.g. `-55`) if it never finds it.
- `lightLevel() < 15`: how dark before it sleeps.

## Words this week

| Word | What it means | Say it to your kid |
| --- | --- | --- |
| **Sensor** | A part that lets the robot notice the world: light, heat, distance, sound, movement. | The robot's eyes, ears and skin. |
| **Behavior** | One thing the robot does in response to something, like 'back away when it's loud'. | Something the robot does when something happens. |
| **Radio** | micro:bits can send short messages to each other through the air, no wires needed, across a house. | Invisible messages through the air. |
| **Signal strength** | How strong a radio message is when it arrives. Closer usually means stronger. | Louder when close, quieter when far. |
| **Whisker sensor** | A springy wire that touches another wire when it bends, closing a circuit the micro:bit can feel. A homemade touch sensor. | When the whisker bumps something, the robot feels it. |
| **Cutebot** | The robot car kit this project uses. The micro:bit slots in as its brain. | Our robot car. |
| **Chassis** | The base of a vehicle that everything else is attached to. | The robot's skeleton. |
| **Ultrasonic sensor** | The two round 'eyes' on the front of the Cutebot. They send out a sound too high to hear and time the echo to measure distance. | The robot squeaks and listens for the echo, like a bat. |
| **V2** | The newer micro:bit, with a speaker, a microphone and a touch-sensitive logo. This project needs it. | The newer micro:bit that can hear and talk. |
| **Servo** | A motor that turns to an exact angle and holds still there, instead of spinning round and round. | A motor that points instead of spins. |
| **S1** | A socket on the Cutebot labeled S1 where you plug in a servo. | The servo's plug spot. |
| **Motor driver board** | A board that gives motors enough power, with the micro:bit telling it what to do. | The muscles helper for the motors. |
| **Gear motor** | A motor with gears inside: slower but stronger, good for turning wheels. | A slow, strong motor for wheels. |
| **RPM** | Revolutions per minute: how many full turns a motor makes in one minute. | How fast a wheel spins. |
| **Volts (V)** | How hard a battery pushes electricity. One AA battery is 1.5 V; two make 3 V. | How strong the battery's push is. |
| **Ball caster** | A small ball in a holder that lets the front of a robot slide in any direction. | A rolling ball foot. |
| **Switch** | Something that opens or closes a gap in a circuit, to turn things off and on. | A little door for electricity: open means off, closed means on. |
| **Jumper wire** | A short wire for connecting parts, often with clips or pins on the ends. | A short connecting wire. |
| **Alligator clip** | A wire with a spring clip at each end, for connecting parts without tools. | A wire with crocodile teeth. |
| **Servo horn** | The small plastic arm that clips onto the servo and moves with it. | The servo's little arm. |
| **Shaft** | The metal rod that sticks out of a motor and spins. | The motor's spinning nose. |
| **Balance** | How weight is spread out. Low and heavy robots are harder to tip over. | Low and heavy is hard to push over. |
| **Pins (P1, P2, GND)** | The metal strips along the micro:bit's bottom edge. P1 and P2 can feel when they're connected to GND (the minus side). | The micro:bit's fingers along the bottom. |

Loading words like *micro:bit*, *MakeCode*, *extension* and *Blocks* are in the [Start here word list](../../START-HERE.md#word-list). All words: [glossary](../../GLOSSARY.md).

## Robot Journal

Draw the mouse and the cheese. Where was the best hiding place?
