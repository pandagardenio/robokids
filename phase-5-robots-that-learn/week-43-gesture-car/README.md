# Week 43 · Gesture-Controlled Car

**Phase 5: Robots That Learn** · ~45 min build + short play sessions during the week · **Skill:** AI → action

## You need

- Laptop + webcam
- Robot car
- Second micro:bit plugged into the laptop as radio relay

## Build together

1. Train classes `go`, `stop`, `left`, `right`, `nothing` (hand gestures the kid invents).
2. Load `relay.ts` onto the USB micro:bit, `main.ts` to the car.
3. Bridge → relay → radio → car.

## Play

Drive the car through the maze using only hand gestures.

## Talk about it

> What happens when the AI is unsure?

## Level up

Add a `dance` gesture.

## Load the program

Each program goes on a different micro:bit. Load them one at a time, with that micro:bit plugged in.

| Program | Goes on | Extension |
| --- | --- | --- |
| [`relay.ts`](relay.ts) | the micro:bit that stays plugged into the laptop | none |
| [`main.ts`](main.ts) | the car | Cutebot |

1. Click the program link, then the **Copy raw file** button (two small squares, top right of the program).
2. Go to [makecode.microbit.org](https://makecode.microbit.org), click **New Project** and name it after the week and program (for example `Week 43 relay`).
3. Click **Extensions** at the bottom of the block list, search `cutebot` and click **Cutebot** (only for programs that need it).
4. Click **JavaScript** at the top, select all the text (**Ctrl+A**, Mac: **Cmd+A**) and paste (**Ctrl+V**, Mac: **Cmd+V**).
5. Click **Blocks** to see the colorful version your kid can change, then click **Download**.

First time, or something went wrong? See [Start here](../../START-HERE.md#load-a-program).

Then open the [AI bridge](https://pandagardenio.github.io/robokids/ai/bridge.html) in Chrome or Edge and follow the [AI bridge guide](../../ai/README.md). Close MakeCode first.

In Teachable Machine, name the classes exactly like this, lowercase: `go`, `left`, `right`, `dance` (plus `nothing`).

## Robot Journal

Draw this week's robot. Write (or dictate) one thing it can do.

---
[← Week 42](../../phase-5-robots-that-learn/week-42-ai-bridge/README.md) · [Week 44 →](../../phase-5-robots-that-learn/week-44-clap-and-whistle-ai/README.md)
