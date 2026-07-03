from modes import free_mode, timed_mode

def header():
    print("=" * 50)
    print("       TYPING SPEED AND ACCURACY TEST")
    print("=" * 50)

def pick_option(prompt, options):
    while True:
        print(prompt)
        for key in options:
            print(f"  {key}. {options[key]}")
        choice = input("\nEnter choice: ").strip()
        if choice in options:
            return choice
        print("  Invalid choice. Try again.\n")

def main():
    while True:
        print()
        header()

        mode = pick_option(
            "\nSelect Mode:",
            {"1": "Timed Mode (race against the clock)",
             "2": "Free Mode (no time limit)"}
        )

        time_limit = None
        if mode == "1":
            t = pick_option(
                "\nSelect Time Limit:",
                {"1": "15 seconds", "2": "30 seconds", "3": "60 seconds",
                 "4": "2 minutes",  "5": "5 minutes",  "6": "10 minutes"}
            )
            time_limit = {"1": 15, "2": 30, "3": 60,
                          "4": 120, "5": 300, "6": 600}[t]

        content_mode = pick_option(
            "\nSelect Content Type:",
            {"1": "Random Sentences", "2": "Random Characters"}
        )

        input("\nPress Enter when ready...")

        if mode == "1":
            result = timed_mode(time_limit, content_mode)
        else:
            result = free_mode(content_mode)

        if not result:
            break

        again = input("\nPlay again? (yes / no): ").strip().lower()
        if again != "yes":
            print("\nThanks for using the Typing Test. Goodbye!\n")
            break

main()
