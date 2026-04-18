# ⌨️ Typing Speed & Accuracy Test

A feature-rich terminal typing test built in Python. Practise your speed and accuracy with live colour-coded feedback, a timed race mode, and detailed performance breakdowns — all in pure standard library.

---

## 📸 Demo

**Timed mode in action:**
```
==================================================
  Time left : 00m 42s
==================================================

  the quick brown fox jumps over the lazy dog

--------------------------------------------------

> the quick brown fox jumps oveR
                              ^
                     (red = wrong char, green = correct)
```

**Results screen:**
```
==================================================
         TIME IS UP!  HERE ARE YOUR RESULTS
==================================================
  Time          : 1m 00s
  Speed         : 58 WPM
  Accuracy      : 94.2%
  Backspaces    : 7
  Sentences Done: 5 & 6/10
  Clean Run     : No (7 corrections made)

  Feedback      : Good job! Keep practicing.
==================================================
```

---

## ✨ Features

- **Two modes** — Timed (race against the clock) and Free (no time pressure)
- **Six time presets** in timed mode — 15s, 30s, 60s, 2min, 5min, 10min
- **Two content types** — curated quotation sentences or random character strings
- **Live colour-coded feedback** — correct characters in green, mistakes in red as you type
- **Cursor navigation** — arrow keys, Home, and End to move through your input
- **Real-time countdown timer** running in a background thread during timed mode
- **Detailed metrics** — WPM, accuracy, backspace count, sentences completed, clean-run bonus
- **Performance feedback** — graded messages based on speed and accuracy combined
- **Cross-platform** — works on Windows (`msvcrt`) and Linux/macOS (`tty`/`termios`)
- **No external dependencies** — pure Python standard library

---

## 📁 Project Structure

```
typing-speed-test/
│
├── main.py      # Entry point — menu and mode selection
├── modes.py     # Timed and Free mode implementations
├── engine.py    # Core input loop, keyboard handling, WPM/accuracy math
└── config.py    # Sentence bank and random character generator
```

---

## 🚀 Getting Started

**Requirements:** Python 3.7+, no external libraries needed.

```bash
# Clone the repository
git clone https://github.com/your-username/typing-speed-test.git
cd typing-speed-test

# Run the test
python main.py
```

> **Best experience:** run in a true terminal (not inside an IDE terminal) so arrow keys and ANSI colours work reliably.

---

## 🎮 Controls

| Key | Action |
|---|---|
| Any character | Type into the input buffer |
| `Backspace` | Delete the character left of cursor (counted as a correction) |
| `←` / `→` | Move cursor left / right |
| `Home` / `End` | Jump to start / end of input |
| `Ctrl+C` | Cancel the current test |

---

## 📊 How Metrics Are Calculated

| Metric | Formula |
|---|---|
| **WPM** | `(correct_characters / 5) / (time_in_minutes)` |
| **Accuracy** | `correct_characters / (total_typed + backspaces) × 100` |
| **Sentences Done** | Count of fully completed sentences + fractional progress on the current one |

The "5 characters = 1 word" standard is used, which matches how most typing tests (Monkeytype, 10fastfingers, etc.) report speed.

---

## 🏆 Grading Thresholds

| WPM | Accuracy | Feedback |
|---|---|---|
| ≥ 60 | ≥ 90% | Excellent! You are a fast typist! |
| ≥ 40 | ≥ 80% | Good job! Keep practicing. |
| ≥ 20 | ≥ 70% | Not bad. Keep going. |
| below | below | Keep practicing. You will improve! |

---

## 🧩 Architecture Notes

- **`engine.py`** holds the platform-specific keyboard reader and the character-by-character input loop. Every keystroke triggers a full redraw of the input line with colour-coding applied based on comparison with the target passage.
- **`modes.py`** wraps the engine for each game mode. Timed mode runs a background thread that updates a live clock in the terminal header using ANSI cursor-save/restore escape codes (`\0337` / `\0338`), so the countdown updates without disturbing what the user is typing.
- **`config.py`** stores a ~90-entry sentence bank (mix of famous quotes, proverbs, and facts) plus a random character generator. A `used` set prevents immediate repetition of sentences within a single timed session.
