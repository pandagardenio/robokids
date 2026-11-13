"""Add a "Words this week" table to every week page and rebuild GLOSSARY.md.

Run from the repo root after editing a week page or the WORDS list below:

    python3 tools/glossary.py

Each entry: (word, regex that finds it on a page, plain meaning, what to say to a kid, weeks to skip).
A word is listed on a week only if its regex matches that week's own text (title, materials,
steps, play, questions). The generic "Load the program" steps are ignored: those words live in
START-HERE.md's word list.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

WORDS = [
    # ---- Electricity and building ----
    ("Circuit", r"circuit", "A complete loop that electricity travels around: out of the battery, through the parts, and back in. Any gap stops everything.", "A round trip for electricity. If the path is broken, nothing works.", ()),
    ("LED", r"\bLEDs?\b(?! screen| editor)", "A tiny light. It only works one way round: the long leg goes to plus (+).", "A tiny light that only works the right way round.", ()),
    ("Coin cell (CR2032)", r"coin cell|CR2032", "A flat, round battery the size of a big button. Dangerous if swallowed: grown-ups handle it (see [Safety](SAFETY.md)).", "A flat battery. Only grown-ups hold it.", ()),
    ("Plus (+) and minus (−)", r"\+ side|\+ line", "The two ends of a battery. Electricity leaves from one end and has to find its way back to the other.", "The battery's way out and way back in.", ()),
    ("Copper tape", r"copper tape", "Sticky metal tape that electricity can travel along, like a flat wire.", "Sticky tape that electricity can walk on.", ()),
    ("Switch", r"\b[Ss]witch(es)?\b(?! roles)(?! on)", "Something that opens or closes a gap in a circuit, to turn things off and on.", "A little door for electricity: open means off, closed means on.", ()),
    ("Series", r"\b[Ss]eries\b", "Parts connected one after the other in a single line. They share the battery's push, so LEDs glow dimmer, and if one goes out they all do.", "Holding hands in a line: everyone shares.", ()),
    ("Parallel", r"\b[Pp]arallel\b", "Parts connected side by side, each with its own path to the battery. LEDs glow brighter, and one going out doesn't stop the others.", "Everyone gets their own path.", ()),
    ("Alligator clip", r"[Aa]lligator|crocodile", "A wire with a spring clip at each end, for connecting parts without tools.", "A wire with crocodile teeth.", ()),
    ("Volts (V)", r"\d\s?V\b", "How hard a battery pushes electricity. One AA battery is 1.5 V; two make 3 V.", "How strong the battery's push is.", ()),
    ("Vibration motor", r"vibration motor", "A tiny motor with a lopsided weight that makes it shake, like a phone buzzing.", "A motor that shakes instead of spins.", ()),
    ("DC motor", r"DC motors?", "A motor that spins when connected to a battery. Swap its two wires and it spins the other way.", "A spinner that runs on batteries.", ()),
    ("Gear motor", r"gear motors?", "A motor with gears inside: slower but stronger, good for turning wheels.", "A slow, strong motor for wheels.", ()),
    ("Shaft", r"\bshafts?\b", "The metal rod that sticks out of a motor and spins.", "The motor's spinning nose.", ()),
    ("Off-center", r"off-center|[Uu]nbalanced", "Weight that isn't in the middle of something spinning, which makes it wobble and shake.", "Lopsided, so it wobbles.", ()),
    ("Chassis", r"chassis", "The base of a vehicle that everything else is attached to.", "The robot's skeleton.", ()),
    ("Axle", r"\baxles?\b", "The rod that wheels turn on.", "The stick the wheels spin on.", ()),
    ("Propeller", r"propeller", "Spinning blades that push air one way, so the vehicle moves the other way.", "Spinning blades that push air.", ()),
    ("Ball caster", r"ball caster", "A small ball in a holder that lets the front of a robot slide in any direction.", "A rolling ball foot.", ()),
    ("Balance", r"\b[Bb]alance|heavier", "How weight is spread out. Low and heavy robots are harder to tip over.", "Low and heavy is hard to push over.", ()),

    # ---- micro:bit ideas ----
    ("Input", r"\b[Ii]nputs?\b", "Something that goes into the robot: a button press, a shake, light, sound.", "What the robot feels.", ()),
    ("Output", r"\b[Oo]utputs?\b", "Something the robot does: lights, sounds, moving.", "What the robot does.", ()),
    ("LED screen", r"LED screen|LED editor|screen fills", "The 25 little lights on the front of the micro:bit that show pictures, numbers and letters.", "The robot's face.", ()),
    ("Icon", r"\bicons?\b", "A small picture shown on the LED screen, like a heart or a smiley.", "A tiny picture made of lights.", ()),
    ("V2", r"\bV2\b", "The newer micro:bit, with a speaker, a microphone and a touch-sensitive logo. This project needs it.", "The newer micro:bit that can hear and talk.", ()),
    ("Sensor", r"\bsensors?\b", "A part that lets the robot notice the world: light, heat, distance, sound, movement.", "The robot's eyes, ears and skin.", ()),
    ("Accelerometer", r"accelerometer|\bshak(e|en|ing)\b|\btilt", "The sensor that feels movement: shaking, tilting, falling.", "It feels when you shake or tip the robot.", ("week-06-scribble-bot",)),
    ("Random", r"[Rr]andom", "Picked by chance, so nobody (not even the robot) knows what comes next.", "Like rolling a dice.", ()),
    ("Loop", r"\bloops?\b|forever|repeat \d", "Instructions that repeat. *Forever* repeats until the power goes off; *repeat 4* does it four times.", "Do it again, and again, and again.", ("week-01-led-robot-eyes", "week-26-line-follower")),
    ("Timing", r"[Tt]iming|turn time|changes? the time", "How long the robot waits or does something. In programs it's often in milliseconds: 1000 = 1 second.", "How long it waits.", ()),
    ("Temperature", r"[Tt]emperature|°C", "How hot or cold something is, in degrees Celsius (°C). A comfy room is about 20 °C.", "How hot or cold.", ()),
    ("Compass", r"[Cc]ompass|[Mm]agnetic", "The micro:bit has a sensor that feels the Earth's magnetism, like a compass needle, so it knows where north is.", "It always knows which way is north.", ()),
    ("Calibration", r"calibrat", "Setting up a sensor so it measures correctly. The compass asks for it the first time.", "Teaching the sensor where things are.", ()),
    ("Light sensor", r"light sensor|measure it", "The micro:bit's LED screen can also measure how bright the room is.", "The robot's face can also see light.", ()),
    ("Sequence", r"[Ss]equence|order of the notes", "Things done in a fixed order. Change the order and you get a different result.", "First this, then that.", ()),
    ("If / else", r"if/else", "The program checks something: IF it's true, do one thing, ELSE (otherwise) do another.", "If it rains, take an umbrella, else take sunglasses.", ()),
    ("Radio", r"\b[Rr]adio\b", "micro:bits can send short messages to each other through the air, no wires needed, across a house.", "Invisible messages through the air.", ()),
    ("Radio group", r"radio group", "A channel number. Only micro:bits set to the same number hear each other.", "A secret channel number.", ()),
    ("Code", r"\bthe code\b|in code\b", "Another word for the program: the instructions the robot follows.", "The robot's instructions.", ()),
    ("Bug", r"\bbug\b", "A mistake that makes a robot do the wrong thing. Finding and fixing it is called debugging.", "A mistake we get to find and fix.", ()),

    # ---- Robot car ----
    ("Cutebot", r"Cutebot", "The robot car kit this project uses. The micro:bit slots in as its brain.", "Our robot car.", ()),
    ("Motor speed", r"[Mm]otor speed|change the speed", "How fast the wheels turn, from 0 (stopped) to 100 (full speed). Negative numbers drive backwards.", "How fast the wheels spin.", ()),
    ("Event", r"\bEvents\b|which button was pressed", "Something that happens, like a button press or a shake, and the instructions that run when it does.", "When this happens, do that.", ()),
    ("RGB", r"RGB|red, green, blue", "Red, Green, Blue. Mixing these three colors of light makes every other color.", "Three colors that mix into all the others.", ()),
    ("Line sensor", r"[Ll]ine follower|leaving the line|on the line", "Two small sensors under the car that see whether the floor below is dark or light.", "The robot's eyes looking at the floor.", ()),
    ("Ultrasonic sensor", r"[Uu]ltrasonic|[Dd]istance sensor|sees a wall|closer than|within \d+ cm|\d+ cm from|Keeping distance", "The two round 'eyes' on the front of the Cutebot. They send out a sound too high to hear and time the echo to measure distance.", "The robot squeaks and listens for the echo, like a bat.", ()),
    ("List", r"moves list|`SCENES` list", "A set of items in order. The program goes through them one by one.", "Like a shopping list for the robot.", ()),

    # ---- Smarter robots ----
    ("Servo", r"\bservo\b", "A motor that turns to an exact angle and holds still there, instead of spinning round and round.", "A motor that points instead of spins.", ()),
    ("Servo horn", r"servo horn", "The small plastic arm that clips onto the servo and moves with it.", "The servo's little arm.", ()),
    ("S1", r"\bS1\b", "A socket on the Cutebot labeled S1 where you plug in a servo.", "The servo's plug spot.", ()),
    ("Microphone", r"microphone|\bmic\b|[Ss]ound sensor|how loud|[Ll]oudness", "The micro:bit V2 can measure how loud it is. It hears loudness, not words.", "The robot's ear. It hears loud and quiet, not words.", ()),
    ("Armed", r"to arm\b|'armed'", "Switched on and watching, ready to sound the alarm.", "On guard.", ()),
    ("State", r"\b[Ss]tates\b", "The mode the robot is in right now, like sleeping, guarding or alarm. It acts differently in each.", "The robot's mood right now.", ()),
    ("Behavior", r"[Bb]ehaviors?", "One thing the robot does in response to something, like 'back away when it's loud'.", "Something the robot does when something happens.", ()),
    ("Signal strength", r"[Ss]ignal", "How strong a radio message is when it arrives. Closer usually means stronger.", "Louder when close, quieter when far.", ()),
    ("Beacon", r"\bbeacon\b", "A micro:bit that keeps sending the same radio message so another one can find it.", "A hidden micro:bit that keeps calling 'I'm here!'.", ()),
    ("Geometry", r"[Gg]eometry|full circle", "The maths of shapes. A full turn is 360°; a square has four turns of 90°.", "Shapes and turns.", ()),

    # ---- AI ----
    ("AI", r"\bAI\b", "Artificial intelligence: a computer program that learns from examples instead of following rules someone wrote.", "A computer that learns by looking at examples.", ()),
    ("Teachable Machine", r"Teachable Machine", "A free Google website where you teach an AI by showing it examples with the webcam or microphone.", "The website where we teach the computer.", ()),
    ("Training", r"\b[Tt]rain", "Showing the AI lots of examples so it learns to tell things apart.", "Teaching the AI by showing it.", ()),
    ("Class", r"\bclass(es)?\b", "One of the things the AI learns to tell apart, like `thumbsup` or `teddy`. Names must match the week's page exactly.", "One thing the AI learns to spot.", ()),
    ("Model", r"\bmodels?\b", "What the AI ends up with after training: its 'memory' of what it learned. Exporting it gives you a link.", "The AI's memory.", ()),
    ("Examples / data", r"\bexamples\b|photos per class|\bdata\b", "The photos or sounds you show the AI. More, varied examples make a smarter AI; few or similar ones make a confused one.", "The pictures we show the AI to learn from.", ()),
    ("Confidence", r"unsure|confiden|how sure", "How sure the AI is about its guess. The bridge only tells the robot when the AI is sure enough.", "How sure the AI is.", ()),
    ("Export", r"Export", "In Teachable Machine: saving the trained model online so you get a link to paste into the AI bridge.", "Sending the AI's memory to the internet so the robot can use it.", ()),
    ("AI bridge", r"[Bb]ridge", "A page from this project that passes what the AI sees or hears to the micro:bit. See the [AI bridge guide](ai/README.md).", "The messenger between the AI and the robot.", ()),
    ("USB", r"\bUSB\b", "The cable between the laptop and the micro:bit. It carries messages, not just power.", "The cable that lets the laptop talk to the robot.", ()),
    ("Relay", r"\brelay\b", "A micro:bit in the middle that passes messages on: it gets them from the laptop by USB and sends them to the car by radio.", "A messenger in the middle.", ()),
    ("Background Noise", r"Background Noise", "A class of normal room sounds in a Teachable Machine audio project, so the AI knows what 'nothing special' sounds like.", "What quiet sounds like.", ()),
    ("AI assistant", r"AI assistant|asks an AI", "A chat tool like Claude or ChatGPT. At this age, the parent types and reads.", "A computer helper that writes words.", ()),
    ("Speech", r"speaks|`say:`|[Tt]alking robot|Speech output", "The laptop reads text out loud with a computer voice.", "The laptop reads the robot's words out loud.", ()),
    ("Template", r"\btemplate\b", "A ready-made program with empty slots to fill in.", "A robot program with blanks to fill.", ()),

    # ---- Bonus: DIY mouse ----
    ("Whisker sensor", r"[Ww]hiskers?", "A springy wire that touches another wire when it bends, closing a circuit the micro:bit can feel. A homemade touch sensor.", "When the whisker bumps something, the robot feels it.", ()),
    ("Pins (P1, P2, GND)", r"\bGND\b|\bP1\b", "The metal strips along the micro:bit's bottom edge. P1 and P2 can feel when they're connected to GND (the minus side).", "The micro:bit's fingers along the bottom.", ()),
    ("Motor driver board", r"[Mm]otor [Dd]river", "A board that gives motors enough power, with the micro:bit telling it what to do.", "The muscles helper for the motors.", ()),
    ("RPM", r"\bRPM\b", "Revolutions per minute: how many full turns a motor makes in one minute.", "How fast a wheel spins.", ()),
    ("Jumper wire", r"jumper wire", "A short wire for connecting parts, often with clips or pins on the ends.", "A short connecting wire.", ()),
]

HEADING = "## Words this week"
LOAD_WORDS = "Loading words like *micro:bit*, *MakeCode*, *extension* and *Blocks* are in the [Start here word list]({up}START-HERE.md#word-list). All words: [glossary]({up}GLOSSARY.md)."
NO_LOAD = "All words: [glossary]({up}GLOSSARY.md)."


def own_text(page: str) -> str:
    """The parts of a week page that are specific to that week."""
    text = re.sub(r"^## (Load the programs?|Words this week)\n.*?(?=^## |^---$)", "", page, flags=re.S | re.M)
    text = re.sub(r"^## Robot Journal\n.*", "", text, flags=re.S | re.M)
    text = re.sub(r"\]\([^)]*\)", "]", text)  # ignore link targets
    return text


def fix_links(text: str, up: str) -> str:
    return re.sub(r"\]\((?!http)([^)]+)\)", lambda m: f"]({up}{m.group(1)})", text)


def main():
    pages = sorted(ROOT.glob("phase-*/week-*/README.md")) + [ROOT / "bonus/robot-mouse/README.md"]
    used = {}
    for page in pages:
        week = page.parent.name
        up = "../../"
        content = page.read_text()
        text = own_text(content)
        found = []
        for word, pattern, meaning, kid, skip in WORDS:
            if week in skip:
                continue
            m = re.search(pattern, text)
            if m:
                found.append((m.start(), word, meaning, kid))
                used.setdefault(word, []).append(page)
        found.sort()
        lines = [HEADING, ""]
        if found:
            lines += ["| Word | What it means | Say it to your kid |", "| --- | --- | --- |"]
            lines += [f"| **{w}** | {fix_links(meaning, up)} | {kid} |" for _, w, meaning, kid in found]
            lines.append("")
        has_program = "## Load the program" in content
        lines += [(LOAD_WORDS if has_program else NO_LOAD).format(up=up), "", ""]
        section = "\n".join(lines)
        if not found:
            section = ""
        if HEADING in content:
            content = re.sub(rf"^{HEADING}\n.*?(?=^## |^---$)", section, content, flags=re.S | re.M)
        elif not section:
            pass
        elif "\n## Robot Journal" in content:
            content = content.replace("\n## Robot Journal", "\n" + section.rstrip("\n") + "\n\n## Robot Journal", 1)
        else:
            content = content.replace("\n---\n", "\n" + section + "---\n", 1)
        page.write_text(content)

    out = ["# Glossary", "",
           "Every technical word used in the weekly projects, in plain language, with a way to say it to your kid. "
           "Each week's page also has a **Words this week** table with just the words it uses. "
           "Words about loading programs (micro:bit, MakeCode, extension, Blocks) are in the [Start here word list](START-HERE.md#word-list).", "",
           "| Word | What it means | Say it to your kid | Weeks |", "| --- | --- | --- | --- |"]
    for word, _, meaning, kid, _ in sorted(WORDS, key=lambda w: w[0].lower()):
        if word not in used:
            continue
        refs = []
        for p in used[word]:
            name = p.parent.name
            label = str(int(name[5:7])) if name.startswith("week-") else "bonus"
            refs.append(f"[{label}]({p.relative_to(ROOT).as_posix()})")
        out.append(f"| **{word}** | {meaning} | {kid} | {', '.join(refs)} |")
    out += ["", "[← Back to the calendar](README.md)", ""]
    (ROOT / "GLOSSARY.md").write_text("\n".join(out))
    unused = [w[0] for w in WORDS if w[0] not in used]
    if unused:
        print("Not found on any page:", ", ".join(unused))


if __name__ == "__main__":
    main()
