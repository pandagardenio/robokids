# 👋 Start here

**You don't need to know how to code.** Every program in this project is ready to use. You copy it into a free website, press a button, and it goes onto your robot. Your kid then changes the numbers and pictures to make it their own.

This page gets your laptop ready in about 15 minutes. You do it once.

> **Weeks 1–10 don't need a laptop at all** (just LEDs, batteries and motors). You can start [week 1](phase-1-circuits-and-motors/week-01-led-robot-eyes/README.md) today and come back here before week 11.

## What you need

- A laptop or desktop: **Windows 10/11, Mac, Linux or Chromebook**. Phones and tablets won't work for loading programs.
- **Google Chrome or Microsoft Edge.** Safari and Firefox can't talk to the micro:bit.
- A **BBC micro:bit V2** with its USB cable (see [Materials](MATERIALS.md)).
- Internet.

Nothing else to install. Everything happens in the browser.

## The steps

1. [Get your AI helper ready](#get-your-ai-helper-ready) (optional but recommended)
2. [Get the right browser](#get-the-right-browser)
3. [Linux only: allow the micro:bit](#linux-only-allow-the-microbit)
4. [Plug in the micro:bit](#plug-in-the-microbit)
5. [Connect the micro:bit to MakeCode](#connect-the-microbit-to-makecode)
6. [Load a program](#load-a-program) (this is what you'll do every week)
7. [Later: the robot car (week 21)](#later-the-robot-car-week-21)
8. [Later: the AI weeks (week 41)](#later-the-ai-weeks-week-41)

Stuck? See [When something goes wrong](#when-something-goes-wrong) and the [word list](#word-list).

---

## Get your AI helper ready

If you use Claude, ChatGPT or another AI assistant, it can walk you through any step, one click at a time. Copy this message, fill in the brackets and send it:

```text
I'm a parent with no coding experience. My 6-year-old and I are doing
"A Year of Robots": https://github.com/pandagardenio/robokids
Please read START-HERE.md and the page for week [NUMBER].
My computer is [Windows / Mac / Linux / Chromebook] and I use [Chrome / Edge].
Guide me one small step at a time, in plain words with no jargon.
Wait until I say "done" before giving me the next step.
```

If your assistant says it can't open links, open the week's page, select all the text (**Ctrl+A**, or **Cmd+A** on a Mac), copy it and paste it under your message.

**Other useful things to ask:**

- "The micro:bit shows [describe what you see]. What does it mean and what do I do?"
- "My kid wants the robot to [go faster / play a different song / show a cat]. Which number or block do we change?" (paste the program too)
- "Turn this week's page into a one-page printable activity card for a 6-year-old."
- "Translate this week's page into [language]."
- "I have a [DFRobot Maqueen / other car] instead of a Cutebot. Change this MakeCode program so it works with it." (paste the program too)

## Get the right browser

| Your computer | What to do |
| --- | --- |
| **Windows** | Microsoft Edge is already installed. Use it, or install [Google Chrome](https://www.google.com/chrome/). |
| **Mac** | Install [Google Chrome](https://www.google.com/chrome/) (or [Edge](https://www.microsoft.com/edge)). Safari won't work. |
| **Linux** | Install [Google Chrome](https://www.google.com/chrome/) from its website (pick the `.deb` file for Ubuntu/Mint/Debian, `.rpm` for Fedora). Chromium from an app store "snap" often can't see USB devices. |
| **Chromebook** | Chrome is already there. Nothing to do. |

From now on, open every link in this project with that browser.

## Linux only: allow the micro:bit

Skip this on Windows, Mac and Chromebook.

Linux blocks websites from talking to USB devices until you allow it, once. Open the **Terminal** app, paste these lines (right-click → Paste), press **Enter** and type your computer password when asked (nothing shows while you type; that's normal):

```bash
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="0d28", MODE="0666"
KERNEL=="ttyACM*", ATTRS{idVendor}=="0d28", MODE="0666"' | sudo tee /etc/udev/rules.d/50-microbit.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Then unplug and replug the micro:bit. You never need to do this again.

## Plug in the micro:bit

1. Connect the micro:bit to the laptop with its USB cable. A small yellow light on the back turns on.
2. A new drive called **MICROBIT** appears, like a USB stick:
   - **Windows:** File Explorer → *This PC*.
   - **Mac:** Finder, in the sidebar (or on the desktop).
   - **Linux:** the Files app, in the sidebar.
   - **Chromebook:** the Files app, in the sidebar.

If no light turns on or no MICROBIT drive appears, **try another cable**. Many phone cables only charge and can't carry data. The cable in the micro:bit box works.

## Connect the micro:bit to MakeCode

[MakeCode](https://makecode.microbit.org) is the free website where programs are loaded and where your kid will drag colorful blocks. You connect it once per browser; after that, one click sends a program to the micro:bit.

1. Open [makecode.microbit.org](https://makecode.microbit.org) and click **New Project**. Name it `Test` and click **Create**.
2. Next to the purple **Download** button at the bottom left, click the **⋯** (three dots) button and choose **Connect device**.
3. Follow the on-screen steps. When the browser shows a list, pick **BBC micro:bit CMSIS-DAP** and click **Connect**.
4. The Download button now shows a little USB icon. You're connected.

If connecting doesn't work, that's fine: you can always use the [drag-and-drop way](#the-drag-and-drop-way) instead. It does the same thing.

## Load a program

This is what you do every week from week 11 on. Each week's page has a **Load the program** section with these same steps and a link to that week's program.

1. **Copy the program.** On the week's page, click the program link (for example `main.ts`). GitHub shows the program. Click the **Copy raw file** button: two small overlapping squares at the top right of the program.
   *Can't find it?* Click **Raw** instead, then select all (**Ctrl+A** / **Cmd+A**) and copy (**Ctrl+C** / **Cmd+C**).
2. **Make a new project.** Go to [makecode.microbit.org](https://makecode.microbit.org), click **New Project** and name it after the week (for example `Week 11`).
3. **Car weeks only: add the Cutebot blocks.** If the week page says so, see [the robot car](#later-the-robot-car-week-21) below.
4. **Paste it.** At the top of MakeCode, click **JavaScript**. Click inside the text, select everything (**Ctrl+A** / **Cmd+A**) and paste (**Ctrl+V** / **Cmd+V**). The old text is replaced.
5. **See the blocks.** Click **Blocks** at the top. Now you see the colorful version. This is where your kid changes numbers, pictures and sounds.
6. **Send it.** Click **Download**.
   - If you [connected the micro:bit](#connect-the-microbit-to-makecode), the program goes straight onto it. Done!
   - If not, use [the drag-and-drop way](#the-drag-and-drop-way).

You can try the program on the **picture of a micro:bit on the left** of MakeCode before sending it. Click its buttons with the mouse.

### The drag-and-drop way

When you click **Download** without a connected micro:bit, MakeCode saves a file whose name ends in `.hex` (for example `microbit-Week-11.hex`) to your **Downloads** folder.

1. Open your **Downloads** folder (Windows: File Explorer; Mac and Linux: Finder / Files; Chromebook: Files).
2. Drag the `.hex` file onto the **MICROBIT** drive.
3. The yellow light blinks for a few seconds, then the program starts.

All normal: the MICROBIT drive disappears and comes back, the file doesn't stay on it, and a Mac may say the disk "wasn't ejected properly". Ignore those.

### Changing things (the knobs)

Every program has a few numbers at the top: speed, time, distance, sounds. These are your kid's **knobs**. In **Blocks**, click a number, type a new one, then click **Download** again. That's all "coding" means at this age.

### Unplugging

The program stays on the micro:bit after you unplug the USB cable. Plug in the battery pack and it runs anywhere.

### Finding old projects

MakeCode saves every project inside your browser. Its home page shows them under **My Projects**. Use the same browser on the same laptop each time, and don't clear the browser's data, or you'll lose them. Since the programs live here in this project, you can always copy them again.

## Later: the robot car (week 21)

The car (Elecfreaks **Cutebot**) needs extra blocks in MakeCode, called an **extension**. In car weeks, after making the new project (step 2 above) and **before pasting**:

1. In the list of block colors on the left, scroll to the bottom and click **Extensions** (or use the ⚙ menu at the top right → **Extensions**).
2. Type `cutebot` in the search box and press **Enter**.
3. Click the **Cutebot** card (not "Cutebot Pro"). You're back in the editor with a new **Cutebot** block color.

Then paste the program as usual. If you forget this, the pasted program shows red underlines and won't download: make a new project and add the extension first.

To load a program onto the car, take the micro:bit out of the car, plug it into the laptop, load the program, then put it back.

## Later: the AI weeks (week 41)

In weeks 41–50 your kid trains a small AI on the laptop, and the robot reacts to it.

- **Teachable Machine** ([teachablemachine.withgoogle.com](https://teachablemachine.withgoogle.com)) is the free website where your kid trains the AI. When the browser asks to use the camera or microphone, click **Allow**.
- **The AI bridge** ([open it here](https://pandagardenio.github.io/robokids/ai/bridge.html)) is a page from this project that passes what the AI sees to the micro:bit. See the [AI bridge guide](ai/README.md) for step-by-step instructions.
- Before opening the bridge, **close the MakeCode tab**. Only one page can talk to the micro:bit at a time.

## When something goes wrong

Say "great, we found a bug!" and check in this order: **batteries → cable → the right program loaded → ask your AI helper**.

| What you see | What to do |
| --- | --- |
| No MICROBIT drive, no yellow light | Try another USB cable (some only charge). Try another USB port. |
| **Connect device** finds nothing | Close other MakeCode tabs and the AI bridge, unplug and replug, try again. On Linux, do [the Linux step](#linux-only-allow-the-microbit). Or use [drag and drop](#the-drag-and-drop-way). |
| Red underlines after pasting, Download doesn't work | Car week? Make a new project and [add the Cutebot extension](#later-the-robot-car-week-21) *before* pasting. Otherwise, copy the program again; part of it may be missing. |
| Blocks look grey, or the page says it can't convert to Blocks | The program still works. Click **Download** anyway. |
| The micro:bit shows a sad face and numbers | Write down the numbers and ask your AI helper. Usually the program for a car was loaded onto a micro:bit that isn't in the car, or batteries are low. |
| The car doesn't move but the micro:bit screen works | Turn on the car's power switch and check its 3 AAA batteries. |
| Download finished but nothing changed on the micro:bit | Press the reset button on the back of the micro:bit. |
| Week 15 asks you to "tilt to fill the screen" | That's normal (it's how the compass sets itself up). Tilt until every light is on. |
| Programs were lost | Copy them again from this project. Your kid's changes may be gone; make them again together. |

## Word list

| Word | Means |
| --- | --- |
| **micro:bit** | The small programmable board with 25 lights and two buttons. The robot's brain. |
| **MakeCode** | The free website where you load programs and your kid edits blocks. |
| **Program** | Instructions for the micro:bit. In this project they're the files ending in `.ts`. You never need to read them. |
| **Load / Download / Flash** | Send a program to the micro:bit. Other guides on the internet often say "flash". |
| **Blocks / JavaScript** | Two views of the same program in MakeCode. You paste into JavaScript; your kid plays in Blocks. |
| **`.hex` file** | What MakeCode downloads. Drag it onto the MICROBIT drive to load it. |
| **Extension** | Extra blocks for a specific gadget, like the Cutebot car. |
| **Knobs** | The numbers at the top of a program that your kid changes. |
| **Teachable Machine** | Free website where your kid teaches an AI by showing examples. |
| **Class** | One thing the AI learns to recognize, like "thumbs up". |
| **AI bridge** | The page in this project that connects the AI to the micro:bit. |

---

[← Back to the calendar](README.md)
