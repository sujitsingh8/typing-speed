import os
import sys
import platform
from settings import WIDTH, HEIGHT, EMPTY, FOOD, DELAY_EASY, DELAY_MEDIUM, DELAY_HARD

# ── Keyboard input setup (depends on OS) ──────────────────────────────────

ON_WINDOWS = platform.system() == "Windows"

if ON_WINDOWS:
    import msvcrt
else:
    import tty
    import termios
    import select


def get_key():
    if ON_WINDOWS:
        if msvcrt.kbhit():
            return msvcrt.getwch().lower()
        return None
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            rlist, _, _ = select.select([sys.stdin], [], [], 0)
            if rlist:
                return sys.stdin.read(1).lower()
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


# ── Screen utilities ───────────────────────────────────────────────────────

def clear():
    """Clear the terminal screen."""
    os.system("cls" if ON_WINDOWS else "clear")


def draw(snake, food, score, high_score, level):
    """
    Build the full game grid and print it in one shot (avoids flicker).
      1. Create empty 2D grid
      2. Place food and snake on it
      3. Convert to string with borders and print
    """
    # Empty 2D grid — grid[row][col]
    grid = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

    # Place food
    fc, fr = food.position
    grid[fr][fc] = FOOD

    # Place snake segments
    for col, row, symbol in snake.get_symbols():
        if 0 <= row < HEIGHT and 0 <= col < WIDTH:
            grid[row][col] = symbol

    # Build output lines
    lines = []
    lines.append("┌" + "─" * (WIDTH * 2) + "┐")
    for row in grid:
        lines.append("│" + "".join(cell + " " for cell in row) + "│")
    lines.append("└" + "─" * (WIDTH * 2) + "┘")
    lines.append(f"  Score : {score}   Best : {high_score}   Level : {level}")
    lines.append(f"  W A S D to move  |  Q to quit")

    clear()
    print("\n".join(lines))


# ── Menu & Game Over screens ───────────────────────────────────────────────

def show_menu():
    """Show the main menu. Returns (delay, level_name)."""
    clear()
    print("""
  ╔══════════════════════════════╗
  ║        🐍  SNAKE  🐍        ║
  ║       Terminal Edition       ║
  ╚══════════════════════════════╝

  Choose Difficulty:
    1 → Easy
    2 → Medium
    3 → Hard

  Controls : W (up)  S (down)  A (left)  D (right)
    """)

    while True:
        choice = input("  Enter 1 / 2 / 3 : ").strip()
        if choice == "1": return DELAY_EASY,   "Easy"
        if choice == "2": return DELAY_MEDIUM, "Medium"
        if choice == "3": return DELAY_HARD,   "Hard"
        print("  Please enter 1, 2, or 3.")


def show_game_over(score, high_score):
    """Show game over screen. Returns True to replay, False to quit."""
    clear()
    print(f"""
  ╔══════════════════════════════╗
  ║         GAME  OVER           ║
  ╚══════════════════════════════╝

  Your Score  : {score}
  High Score  : {high_score}
    """)

    while True:
        choice = input("  Play again? (Y / N) : ").strip().lower()
        if choice == "y": return True
        if choice == "n": return False
        print("  Please enter Y or N.")
