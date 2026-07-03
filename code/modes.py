import sys
import time
import random
import threading

from config import get_random_chars, get_next_sentence, sentences
from engine import (
    input_loop, calculate_wpm, calculate_accuracy,
    count_correct, format_time, GREEN, RED, RESET
)

#  SHOW RESULTS
def show_result(wpm, accuracy, time_taken, backspaces, sentences_done, timed_out=False):
    print("\n" + "=" * 50)
    if timed_out:
        print("         TIME IS UP!  HERE ARE YOUR RESULTS")
    else:
        print("                  YOUR RESULTS")
    print("=" * 50)
    print(f"  Time          : {format_time(time_taken)}")
    print(f"  Speed         : {wpm} WPM")
    print(f"  Accuracy      : {accuracy}%")
    print(f"  Backspaces    : {backspaces}")

    if sentences_done > 0:
        full = int(sentences_done)
        fraction = round(sentences_done - full, 1)
        if fraction > 0:
            frac_str = f"{int(fraction * 10)}/10"
            print(f"  Sentences Done: {full} & {frac_str}")
        else:
            print(f"  Sentences Done: {full}")

    if backspaces == 0:
        print("  Clean Run     : Yes! Perfect hands!")
    elif backspaces <= 3:
        print("  Clean Run     : Almost! Very few corrections.")
    else:
        print(f"  Clean Run     : No ({backspaces} corrections made)")

    if wpm >= 60 and accuracy >= 90:
        grade = "Excellent! You are a fast typist!"
    elif wpm >= 40 and accuracy >= 80:
        grade = "Good job! Keep practicing."
    elif wpm >= 20 and accuracy >= 70:
        grade = "Not bad. Keep going."
    else:
        grade = "Keep practicing. You will improve!"

    print(f"\n  Feedback      : {grade}")
    print("=" * 50)

#  FREE MODE
def free_mode(content_mode):
    if content_mode == "1":
        passage = random.choice(sentences)
    else:
        passage = get_random_chars(50)

    print()
    print("-" * 50)
    print(f"  {passage}")
    print("-" * 50)
    print("  Arrow keys move cursor. Backspace tracked.")
    print()

    start_time_ref = [None]
    typed, backspaces, cancelled = input_loop(passage, start_time_ref=start_time_ref)

    if cancelled:
        print("\n\nTest cancelled.")
        return False

    end_time = time.time()
    if start_time_ref[0] is None:
        start_time_ref[0] = end_time
    time_taken = end_time - start_time_ref[0]

    correct  = count_correct(typed, passage)
    wpm      = calculate_wpm(correct, time_taken)
    accuracy = calculate_accuracy(correct, len(typed), backspaces)
    print()
    show_result(wpm, accuracy, time_taken, backspaces, 0)
    return True
    
#  TIMED MODE
def timed_mode(time_limit, content_mode):
    used = set()

    def next_passage():
        if content_mode == "1":
            return get_next_sentence(used)
        return get_random_chars(40)

    def show_screen(passage, remaining, typed="", cursor_pos=0):
        print("\033[2J\033[H", end="")
        print("=" * 50)
        print(f"  Time left : {format_time(remaining)}")
        print("=" * 50)
        print(f"\n  {passage}\n")
        print("-" * 50)
        print()
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

    def make_timer_thread(stop_event, start_time):
        def run():
            while not stop_event.is_set():
                time.sleep(1)
                if stop_event.is_set():
                    break
                remaining = max(0, time_limit - (time.time() - start_time))
                sys.stdout.write(f"\0337\033[2;15H{format_time(remaining)}   \0338")
                sys.stdout.flush()
        t = threading.Thread(target=run, daemon=True)
        t.start()
        return t

    passage        = next_passage()
    backspaces     = 0
    total_correct  = 0
    total_typed    = 0
    sentences_done = 0
    start_time     = time.time()

    show_screen(passage, time_limit)
    stop_timer = threading.Event()
    timer_t    = make_timer_thread(stop_timer, start_time)

    while True:
        if time.time() - start_time >= time_limit:
            stop_timer.set()
            timer_t.join(timeout=1)
            wpm      = calculate_wpm(total_correct, time_limit)
            accuracy = calculate_accuracy(total_correct, total_typed, backspaces)
            print()
            show_result(wpm, accuracy, time_limit, backspaces, sentences_done, timed_out=True)
            return True

        stop_event = threading.Event()

        def clock_watcher(se=stop_event):
            while not se.is_set():
                if time.time() - start_time >= time_limit:
                    se.set()
                    return
                time.sleep(0.1)

        cw = threading.Thread(target=clock_watcher, daemon=True)
        cw.start()

        typed, bs, cancelled = input_loop(passage, stop_event=stop_event)
        stop_event.set()
        cw.join(timeout=0.5)
        backspaces += bs

        if cancelled:
            stop_timer.set()
            timer_t.join(timeout=1)
            print("\n\nTest cancelled.")
            return False

        if time.time() - start_time >= time_limit:
            stop_timer.set()
            timer_t.join(timeout=1)
            correct_now    = count_correct(typed, passage)
            total_correct += correct_now
            total_typed   += len(typed)
            fraction = round(len(typed) / len(passage), 1) if len(passage) > 0 else 0
            wpm      = calculate_wpm(total_correct, time_limit)
            accuracy = calculate_accuracy(total_correct, total_typed, backspaces)
            print()
            show_result(wpm, accuracy, time_limit, backspaces,
                        sentences_done + fraction, timed_out=True)
            return True

        # Sentence completed correctly
        total_correct  += len(typed)
        total_typed    += len(typed)
        sentences_done += 1
        passage = next_passage()

        stop_timer.set()
        timer_t.join(timeout=2)
        stop_timer.clear()

        remaining = max(0, time_limit - (time.time() - start_time))
        show_screen(passage, remaining)
        timer_t = make_timer_thread(stop_timer, start_time)
