import time
from settings import UP, DOWN, LEFT, RIGHT
from models   import Snake, Food
from ui       import get_key, draw, show_menu, show_game_over

# Key → Direction mapping
KEY_MAP = {
    "w": UP,
    "s": DOWN,
    "a": LEFT,
    "d": RIGHT,
}


def run_game(delay, level, high_score):
    snake = Snake()
    food  = Food(snake.body)
    score = 0

    while True:

        # 1. Input
        key = get_key()
        if key == "q":
            break
        if key in KEY_MAP:
            snake.change_direction(KEY_MAP[key])

        # 2. Move
        snake.move()

        # 3. Food
        if snake.body[0] == food.position:
            snake.eat()
            food.respawn(snake.body)
            score += 10
            if score > high_score:
                high_score = score

        # 4. Collisions
        if snake.hit_wall() or snake.hit_self():
            break

        # 5. Draw
        draw(snake, food, score, high_score, level)

        # 6. Wait
        time.sleep(delay)

    return score, high_score


def main():
    high_score = 0

    while True:
        delay, level      = show_menu()
        score, high_score = run_game(delay, level, high_score)
        play_again        = show_game_over(score, high_score)

        if not play_again:
            print("\n  Thanks for playing! 🐍\n")
            break


if __name__ == "__main__":
    main()
