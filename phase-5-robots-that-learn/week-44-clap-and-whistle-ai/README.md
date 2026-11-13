# Week 44 · Clap and Whistle AI

**Phase 5: Robots That Learn** · ~45 min build + short play sessions during the week · **Skill:** Training with sound

## You need

- Laptop with mic
- Robot car + USB relay micro:bit (from week 43)

## Build together

1. Teachable Machine → Audio Project. Classes: `Background Noise` (required), `clap`, `whistle`.
2. Export the model, paste the link into the [AI bridge](https://pandagardenio.github.io/robokids/ai/bridge.html) and choose **Audio**.

## Play

Clap = dance, whistle = come back. Play 'robot dog'.

## Talk about it

> How is this different from week 33 (just loudness)?

## Level up

Add a `snap` sound for spinning.

## Load the program

Program for the car: [`main.ts`](main.ts) · needs the **Cutebot** extension

The micro:bit plugged into the laptop keeps [`relay.ts` from week 43](../week-43-gesture-car/relay.ts). If you reused it for something else, load that again too.

1. Click the program link, then the **Copy raw file** button (two small squares, top right of the program).
2. Go to [makecode.microbit.org](https://makecode.microbit.org), click **New Project** and name it `Week 44`.
3. Click **Extensions** at the bottom of the block list, search `cutebot` and click **Cutebot**.
4. Click **JavaScript** at the top, select all the text (**Ctrl+A**, Mac: **Cmd+A**) and paste (**Ctrl+V**, Mac: **Cmd+V**).
5. Click **Blocks** to see the colorful version your kid can change, then click **Download**.

First time, or something went wrong? See [Start here](../../START-HERE.md#load-a-program).

Then open the [AI bridge](https://pandagardenio.github.io/robokids/ai/bridge.html) in Chrome or Edge and follow the [AI bridge guide](../../ai/README.md). Close MakeCode first.

In Teachable Machine, name the classes exactly like this, lowercase: `clap`, `whistle`, `snap` (plus *Background Noise*).

## Words this week

| Word | What it means | Say it to your kid |
| --- | --- | --- |
| **AI** | Artificial intelligence: a computer program that learns from examples instead of following rules someone wrote. | A computer that learns by looking at examples. |
| **Training** | Showing the AI lots of examples so it learns to tell things apart. | Teaching the AI by showing it. |
| **Microphone** | The micro:bit V2 can measure how loud it is. It hears loudness, not words. | The robot's ear. It hears loud and quiet, not words. |
| **USB** | The cable between the laptop and the micro:bit. It carries messages, not just power. | The cable that lets the laptop talk to the robot. |
| **Relay** | A micro:bit in the middle that passes messages on: it gets them from the laptop by USB and sends them to the car by radio. | A messenger in the middle. |
| **Teachable Machine** | A free Google website where you teach an AI by showing it examples with the webcam or microphone. | The website where we teach the computer. |
| **Background Noise** | A class of normal room sounds in a Teachable Machine audio project, so the AI knows what 'nothing special' sounds like. | What quiet sounds like. |
| **Export** | In Teachable Machine: saving the trained model online so you get a link to paste into the AI bridge. | Sending the AI's memory to the internet so the robot can use it. |
| **Model** | What the AI ends up with after training: its 'memory' of what it learned. Exporting it gives you a link. | The AI's memory. |
| **AI bridge** | A page from this project that passes what the AI sees or hears to the micro:bit. See the [AI bridge guide](../../ai/README.md). | The messenger between the AI and the robot. |

Loading words like *micro:bit*, *MakeCode*, *extension* and *Blocks* are in the [Start here word list](../../START-HERE.md#word-list). All words: [glossary](../../GLOSSARY.md).

## Robot Journal

Draw this week's robot. Write (or dictate) one thing it can do.

---
[← Week 43](../../phase-5-robots-that-learn/week-43-gesture-car/README.md) · [Week 45 →](../../phase-5-robots-that-learn/week-45-toy-sorter/README.md)
