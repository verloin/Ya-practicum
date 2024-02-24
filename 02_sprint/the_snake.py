from random import choice, randint
import sys
import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
START_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
DEFAULT_POSITION = (0, 0)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10

# Изменения направлений
TURNS = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption(
    f'Игра "Змейка".  Для выхода нажмите ESC. Скорость: {SPEED}')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс игровых объектов."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """Конструктор родительского класса, создающий игровые объекты."""
        self.position = START_POSITION
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки игровых объектов."""
        raise NotImplementedError

    def draw_cell(self, position, color=None):
        """Метод для отрисовки ячеек игровой поверхности"""
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        if color != BORDER_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        pg.draw.rect(screen, color, rect)


class Apple(GameObject):
    """Класс описывает Яблоко."""

    def __init__(self, positions=[DEFAULT_POSITION],
                 body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position(positions)

    def randomize_position(self, positions):
        """Устанавливает случайные координаты яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Дочерний класс, описывающий змейку."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Конструктор дочернего класса, создающий змейку."""
        super().__init__(body_color)
        self.reset()

    def update_direction(self, next_direction=None):
        """Метод изменения направления движения."""
        self.direction = next_direction

    def get_head_position(self):
        """Возвращает координаты первого квадрата змейки."""
        return self.positions[0]

    def move(self):
        """Двигает змейку по полю."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        self.positions.insert(
            0,
            (
                (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
            )
        )
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку и затирает последний сегмент."""
        self.draw_cell(self.get_head_position())
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Сбрасывает состояние змейки в исходное положение."""
        self.length = 1
        self.last = None
        self.positions = [START_POSITION]
        self.direction = choice((LEFT, RIGHT, UP, DOWN))


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиши и задает направление движения,
    изменяет скорость движения.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sys.exit()
            next_direction = TURNS.get(
                (game_object.direction, event.key)
            )
            if next_direction:
                game_object.update_direction(next_direction)


def save_record(record):
    """Выводит рекорд сессии и сохраняет в файл"""
    message = f'Session record: {record}.'
    print(message)
    with open('records.txt', 'a') as r:
        r.write(message)


def main():
    """Обрабатывает основной цикл игры."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            sys.exit()
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
