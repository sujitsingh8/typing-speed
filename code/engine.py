import sys
import time

if sys.platform == "win32":
    import msvcrt
else:
    import tty
    import termios
    import select

GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"

#  KEYBOARD INPUT
def get_key():
    if sys.platform == "win32":
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):
            ch2 = msvcrt.getwch()
            if ch2 == "\x4b": return "LEFT"
            if ch2 == "\x4d": return "RIGHT"
            if ch2 == "\x47": return "HOME"
            if ch2 == "\x4f": return "END"
            return ""
        return ch
    else:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                ready = select.select([sys.stdin], [], [], 0.1)[0]
                if not ready:
                    return ""
                ch2 = sys.stdin.read(1)
                ready2 = select.select([sys.stdin], [], [], 0.1)[0]
                if not ready2:
                    return ""
                ch3 = sys.stdin.read(1)
                if ch2 == "[":
                    if ch3 == "D": return "LEFT"
                    if ch3 == "C": return "RIGHT"
                    if ch3 == "H": return "HOME"
                    if ch3 == "F": return "END"
                return ""
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

#  REDRAW INPUT LINE WITH LIVE HIGHLIGHTING
def redraw_input(typed, cursor_pos, passage):
    sys.stdout.write("\r\033[K")
    sys.stdout.write("> ")
    for i in range(len(typed)):
        ch = typed[i]
        if i < len(passage) and ch == passage[i]:
            sys.stdout.write(GREEN + ch + RESET)
        else:
            sys.stdout.write(RED + ch + RESET)
    move_back = len(typed) - cursor_pos
    if move_back > 0:
        sys.stdout.write(f"\033[{move_back}D")
    sys.stdout.flush()

#  CALCULATIONS
def calculate_wpm(correct_chars, seconds):
    words = correct_chars / 5
    minutes = seconds / 60
    if minutes == 0:
        return 0
    return round(words / minutes)

def calculate_accuracy(correct_chars, total_chars_typed, backspaces):
    total_attempts = total_chars_typed + backspaces
    if total_attempts == 0:
        return 0
    return round((correct_chars / total_attempts) * 100, 2)

def count_correct(typed, passage):
    correct = 0
    for i in range(min(len(typed), len(passage))):
        if typed[i] == passage[i]:
            correct += 1
    return correct

def format_time(seconds):
    m = int(seconds) // 60
    s = int(seconds) % 60
    if m > 0:
        return f"{m}m {s:02d}s"
    return f"{s:02d}s"

#  CORE INPUT LOOP
def input_loop(passage, stop_event=None, start_time_ref=None):
    typed = ""
    cursor_pos = 0
    backspaces = 0
    first_key = True

    sys.stdout.write("> ")
    sys.stdout.flush()

    while True:
        if stop_event is not None:
            if stop_event.is_set():
                return typed, backspaces, False
            if sys.platform != "win32":
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    ready = select.select([sys.stdin], [], [], 0.05)[0]
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
                if not ready:
                    continue
            elif sys.platform == "win32":
                if not msvcrt.kbhit():
                    time.sleep(0.05)
                    continue

        key = get_key()

        if first_key and start_time_ref is not None:
            start_time_ref[0] = time.time()
            first_key = False

        if key == "\x03":
            return typed, backspaces, True

        if key in ("\r", "\n"):
            continue

        if key == "LEFT":
            if cursor_pos > 0:
                cursor_pos -= 1
                sys.stdout.write("\033[1D")
                sys.stdout.flush()
            continue

        if key == "RIGHT":
            if cursor_pos < len(typed):
                cursor_pos += 1
                sys.stdout.write("\033[1C")
                sys.stdout.flush()
            continue

        if key == "HOME":
            cursor_pos = 0
            redraw_input(typed, cursor_pos, passage)
            continue

        if key == "END":
            cursor_pos = len(typed)
            redraw_input(typed, cursor_pos, passage)
            continue

        if key in ("\x08", "\x7f"):
            if cursor_pos > 0:
                typed = typed[:cursor_pos - 1] + typed[cursor_pos:]
                cursor_pos -= 1
                backspaces += 1
                redraw_input(typed, cursor_pos, passage)
            continue

        if key == "":
            continue

        typed = typed[:cursor_pos] + key + typed[cursor_pos:]
        cursor_pos += 1
        redraw_input(typed, cursor_pos, passage)

        if typed == passage:
            return typed, backspaces, False
