from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = (320, 240)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
"""Константы для размеров поля и сетки."""

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
"""Направления движения."""

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20
"""Скорость движения змейки."""

pygame.init()
"""Инициализация Pygame."""
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
"""# Настройка игрового окна:."""

pygame.display.set_caption('Змейка')
"""# Заголовок окна игрового поля."""

clock = pygame.time.Clock()
"""Настройка игрового времени."""


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self) -> None:
        """Инициализация базового объекта, установка начальной позиции."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий яблоко и действия c ним.
    """

    def __init__(self, eng_positions=None,
                 position=SCREEN_CENTER,
                 body_color=APPLE_COLOR):
        """Устанавливает базовое положение и цвет объекта."""
        super().__init__()
        self.body_color = body_color
        self.randomize_position(eng_positions)

    def draw(self):
        """Отрисовывает яблоко на поле игры."""
        rect = pygame.Rect(self.position[0] * GRID_SIZE,
                           self.position[1] * GRID_SIZE,
                           GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, eng_positions):
        """Устанавливает случайное положение яблока."""
        if eng_positions is None:
            eng_positions = []
        while True:
            self.position = (randint(0, GRID_WIDTH - 1),
                             randint(0, GRID_HEIGHT - 1))
            if self.position not in eng_positions:
                break


class Snake(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self):
        super().__init__()
        """Инициализация змейки, установка начального цвета и позиции."""

        self.body_color = SNAKE_COLOR
        self.length = 1  # Начальная длина змейки
        self.positions = [(10, 10)]  # Начальная позиция (центр экрана)
        self.direction = (1, 0)  # Направление движения (по умолчанию вправо)
        self.next_direction = None  # Следующее направление
        self.last = None

    def update_direction(self):
        """Метод, который обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, который обновляет позицию змейки.
        Добавляет новую голову
        в начало списка позиций змейки,
        обновляет позицию
        и учитывает границы игрового поля.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        self.last = self.positions[-1]
        new_head = (self.positions[0][0] + self.direction[0],
                    self.positions[0][1] + self.direction[1])
        new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
        """Ограничивает выход за пределы поля."""

        self.positions.insert(0, new_head)
        """Добавление новой головы в начало списка."""

        if len(self.positions) > self.length:
            """Удаление последнего сегмента, если длина не увеличивается"""

            self.positions.pop()

    def get_head_position(self):
        """Метод, который возвращает позицию головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод, который перезапускает игру,
        сбрасывает змейку в начальное состояние.
        """
        self.__init__()

    def draw(self):
        """Метод, отрисовывает змейку на экране."""
        for position in self.positions:
            rect = (pygame.Rect(position[0] * GRID_SIZE,
                                position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0][0] * GRID_SIZE,
                                self.positions[0][1] * GRID_SIZE,
                                GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last[0] * GRID_SIZE,
                                    self.last[1] * GRID_SIZE,
                                    GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры.
    Создает экземпляры класса Snake и Apple, запускает игровой цикл.
    """
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()
        """Обновление экрана."""


if __name__ == '__main__':
    main()
