# AI bridge

In weeks 42–48 your kid's AI (trained in [Teachable Machine](https://teachablemachine.withgoogle.com)) controls the robot. The **AI bridge** is a page from this project that passes what the AI sees or hears to the micro:bit.

```
camera / microphone → your kid's AI → AI bridge page → USB cable → micro:bit
                                                          └─ radio → robot car (weeks 43–44)
```

## Open the bridge

👉 **[Open the AI bridge](https://pandagardenio.github.io/robokids/ai/bridge.html)** in **Chrome or Edge** on a computer. It doesn't work in Safari, Firefox or on phones.

<details>
<summary>The link doesn't open? Use a downloaded copy instead</summary>

1. Open [`bridge.html`](bridge.html) on GitHub and click the **Download raw file** button (an arrow pointing down, top right).
2. Find `bridge.html` in your Downloads folder, right-click it → **Open with** → **Chrome** (or Edge).

</details>

## Use it

**Before you start:** load the week's program onto the micro:bit (see the week's page), keep it plugged into the laptop with its USB cable, and **close the MakeCode tab**. Only one page can talk to the micro:bit at a time.

1. **Get your AI's link.** In Teachable Machine, after training, click **Export Model** → **Upload my model** → **Copy** the link it shows.
2. **In the bridge,** choose the model type (*Image* for the camera, *Audio* for sounds) and paste the link.
3. Click **Connect micro:bit**, pick the micro:bit from the list (it may be called *BBC micro:bit CMSIS-DAP* or *mbed Serial Port*) and click **Connect**. The dot turns green.
4. Click **Start AI** and allow the camera or microphone when the browser asks.

The big word shows what the AI thinks it sees; the micro:bit reacts to it. You can also type a class name in **Test without AI** and click **Send** to check the robot without the AI.

## Tips

- **Name the classes exactly as the week's page says**, lowercase and without spaces (`go`, `thumbsup`). If the names don't match, the robot ignores them.
- **Always add a `nothing` class** (camera models: your kid out of view) or keep **Background Noise** (sound models). It stops the robot doing random things.
- **Robot acting jumpy?** Move the "at least this sure" slider to the right. The bridge then only sends a class when the AI is more confident, and sends `unsure` otherwise.
- **Privacy:** "Upload my model" stores the trained model (not your photos) on Google's servers so the link works. Read Teachable Machine's privacy notes before uploading a model trained on your kid's face.

## Not working?

| What you see | What to do |
| --- | --- |
| "Could not connect" or no micro:bit in the list | Close every MakeCode tab, unplug and replug the micro:bit, try again. On Linux, do the [one-time USB step](../START-HERE.md#linux-only-allow-the-microbit). |
| The camera stays black | Click the camera icon in the address bar and allow the camera. Close other apps using it (video calls). |
| The AI works but the robot doesn't react | Check the class names match the week's page exactly. In weeks 43–44, check the car is switched on and has the week's program. |
| "This page only works in Chrome or Edge" | Open the link in Chrome or Edge on a computer. |
