# AI bridge

[`bridge.html`](bridge.html) connects a [Teachable Machine](https://teachablemachine.withgoogle.com) model to a micro:bit over USB using Web Serial.

```
webcam / mic → Teachable Machine model (in the browser) → bridge.html → USB serial → micro:bit
                                                                           └─ radio → robot car (weeks 43–44)
```

## Use it

1. Download `bridge.html` and open it in **Chrome or Edge** on a computer (Web Serial is not available in Firefox, Safari or on phones). If the browser blocks the camera from a local file, serve the folder: `python3 -m http.server` and open `http://localhost:8000/ai/bridge.html`.
2. In Teachable Machine: **Export Model → Upload my model** → copy the shareable link.
3. Choose the model type, paste the link, click **Connect micro:bit** and pick the micro:bit.
4. Click **Start AI**.

## Protocol

- Bridge → micro:bit: the winning class label plus `\n`, sent only when it changes. If confidence is below the slider, it sends `unsure`.
- micro:bit → bridge: any line starting with `say:` is spoken aloud by the browser (week 48). Other lines are shown in the log.
- Baud rate: 115200.

## Tips

- Name classes in lowercase with no spaces (`go`, `thumbsup`) so they match the code.
- Always add a `nothing` class (image) or keep `Background Noise` (audio). It stops the robot doing random things.
- Close MakeCode tabs that are connected to the micro:bit before connecting the bridge; only one page can use the serial port.
