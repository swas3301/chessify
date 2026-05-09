# ♟ Chessify — Voice Controlled Chess

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Voice-Vosk%20Offline-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Chess.com-Compatible-brightgreen?style=for-the-badge">
</p>

<p align="center">
  <strong>Say a move. Watch it play.</strong>
</p>

**Chessify** is a Python tool that lets you control chess on your screen using your voice.
It detects the board, listens to what you say, and clicks the squares for you.
Everything runs locally — no API keys, no internet required after setup.

> ⚠️ **Fair Use Notice:** This tool is intended for solo practice, puzzles, and offline games only.
> Do **not** use in rated games against other players — see [Fair Use](#fair-use).

---

## How It Works
You speak  →  Vosk hears it  →  Move is parsed  →  Mouse clicks the squares
"e2 to e4"     "e2 to e4"        (e2, e4)            click e2, click e4

1. Opens Firefox and goes to chess.com
2. Detects the chess board on your screen (auto or manual)
3. Listens to your microphone continuously
4. Parses what you said into a move
5. Clicks source square then destination square

---

## Features

- 🎙 **Voice to move** — say "e2 to e4" and it plays it
- 🔍 **Auto board detection** — finds the board using OpenCV
- 🖱 **Manual calibration** — click two corners if auto fails
- 💾 **Saves calibration** — no recalibration needed next run
- 🔄 **Flip board** — supports both white and black perspective
- 🏰 **Castling support** — say "castle kingside" or "long castle"
- 🌐 **NATO alphabet** — say "echo 2 to echo 4" works too
- 📴 **Fully offline** — uses Vosk, no API key needed

---

## Supported Phrases

| You say | What happens |
|---|---|
| `e2 to e4` | moves piece from e2 to e4 |
| `echo 2 to echo 4` | same thing (NATO alphabet) |
| `rook from g7 to g5` | also works |
| `castle kingside` | clicks e1 then g1 |
| `castle queenside` | clicks e1 then c1 |
| `long castle` | same as castle queenside |
| `short castle` | same as castle kingside |
| `flip` | switches white/black view |
| `recalibrate` | redo board detection |
| `quit` | exits the program |

---

## Project Structure
chessify/
├── main.py              ← run this to start
├── detector.py          ← finds the chess board on screen
├── listener.py          ← mic input + move parsing (vosk)
├── executor.py          ← clicks the squares on screen
├── download_model.py    ← run this once to get vosk model
├── test_mic.py          ← test your mic before playing
├── requirements.txt     ← all dependencies
├── calibration.json     ← saved board position (auto-created)
├── vosk-model/          ← created by download_model.py
└── README.md

---

## Requirements

- Python 3.8+
- Firefox installed
- A working microphone
- Linux X11 / Windows / macOS

---

## Installation

**1. Clone the repo**
```bash
git clone https://github.com/yourname/chessify.git
cd chessify
```

**2. Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate        # linux / mac
venv\Scripts\activate           # windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**Linux only — install portaudio first:**
```bash
sudo apt install portaudio19-dev python3-dev
```

**4. Download the Vosk model (50MB, runs once)**
```bash
python3 download_model.py
```

**5. Test your mic**
```bash
python3 test_mic.py
```

**6. Run it**
```bash
python3 main.py
```

---

## First Run

On first launch the program will:

1. Open Firefox and go to chess.com
2. Try to auto-detect the board using OpenCV
3. If that fails — ask you to manually click two corners:
   - hover over top-left of square a8 → press Enter
   - hover over bottom-right of square h1 → press Enter
4. Save position to `calibration.json`
5. Start listening for your voice

From the second run onward calibration is skipped automatically.

---

## Platform Notes

| Platform | Works? | Notes |
|---|---|---|
| Windows | ✅ | works out of the box |
| macOS | ✅ | enable Accessibility in System Preferences |
| Linux X11 | ✅ | install `portaudio19-dev` first |
| Linux Wayland | ❌ | switch to X11 at login screen |

**Check your Linux session type:**
```bash
echo $XDG_SESSION_TYPE   # should say x11
```

**Switch to X11 on Ubuntu:**
log out → click gear ⚙ at login → select **Ubuntu on Xorg** → log in

---

## Troubleshooting

**mouse isn't clicking anything**
- you're probably on Wayland — switch to X11 (see above)

**board not detected automatically**
- wait for chess.com to fully load before the screenshot
- increase `time.sleep(2)` in `detector.py` to `time.sleep(5)`
- use manual calibration when prompted

**voice not recognized**
- run `python3 test_mic.py` to diagnose
- speak closer to your mic
- make sure vosk model is downloaded

**firefox not opening**
- try changing `"firefox"` to `"firefox-esr"` in `detector.py`
- check which one you have: `which firefox` or `which firefox-esr`

**address bar click missing**
- your toolbar might be a different height
- find the exact position:
```bash
python3 -c "import pyautogui, time; time.sleep(3); print(pyautogui.position())"
```
hover over the address bar during those 3 seconds

---

## Fair Use

this tool is built for:
- ✅ solo practice and puzzles
- ✅ playing against chess.com computer bots
- ✅ offline chess engines
- ✅ unrated games where your opponent knows

do **not** use in:
- ❌ rated games against real players
- ❌ tournaments or competitions
- ❌ any game where the other person doesn't know

chess.com's fair play policy prohibits automation in rated games.
full policy: [chess.com/legal/fair-play](https://www.chess.com/legal/fair-play)

---

## Dependencies

| package | what it does |
|---|---|
| `pyautogui` | mouse control + screenshots |
| `opencv-python` | board detection from screenshot |
| `vosk` | offline speech recognition |
| `pyaudio` | microphone access |
| `numpy` | image processing |
| `Pillow` | screenshot handling |
| `requests` | downloading the vosk model |

---

## License

MIT — do whatever you want with it, just don't cheat in rated games. ♟