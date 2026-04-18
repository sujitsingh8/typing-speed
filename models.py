import random
from settings import WIDTH, HEIGHT, RIGHT, SNAKE_HEAD, SNAKE_BODY


class Snake:
    def __init__(self):
        mid_col = WIDTH  // 2
        mid_row = HEIGHT // 2
        self.body      = [(mid_col, mid_row),
                          (mid_col - 1, mid_row),
                          (mid_col - 2, mid_row)]
        self.direction = RIGHT
        self.grow_next = False

    def change_direction(self, new_dir):
        opposite = (-new_dir[0], -new_dir[1])
        if self.direction != opposite:
            self.direction = new_dir

    def move(self):
        head_col, head_row = self.body[0]
        dc, dr = self.direction
        new_head = (head_col + dc, head_row + dr)
        self.body.insert(0, new_head)

        if self.grow_next:
            self.grow_next = False
        else:
            self.body.pop()

    def eat(self):
        self.grow_next = True

    def hit_wall(self):
        col, row = self.body[0]
        return col < 0 or col >= WIDTH or row < 0 or row >= HEIGHT

    def hit_self(self):
        return self.body[0] in self.body[1:]

    def get_symbols(self):
        result = []
        for i, (col, row) in enumerate(self.body):
            symbol = SNAKE_HEAD if i == 0 else SNAKE_BODY
            result.append((col, row, symbol))
        return result


class Food:
    def __init__(self, snake_body):
        self.position = self._random_pos(snake_body)

    def _random_pos(self, snake_body):
        while True:
            col = random.randint(0, WIDTH  - 1)
            row = random.randint(0, HEIGHT - 1)
            if (col, row) not in snake_body:
                return (col, row)

    def respawn(self, snake_body):
        self.position = self._random_pos(snake_body)