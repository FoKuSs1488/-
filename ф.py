import pygame
import sys

# Инициализация pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 400
GRAVITY = 0.5
JUMP_STRENGTH = -10
SPEED = 5

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash")

# Шрифт
font = pygame.font.Font(None, 50)


def show_text(text, y_offset=0):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 + y_offset))
    pygame.display.flip()


# Игровое меню
def main_menu():
    screen.fill(WHITE)
    show_text("Geometry Dash", -50)
    show_text("Нажми пробіл для старта", 50)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


def show_game_over():
    show_text("Ти програв! Нажми R для рестарта")


# Класс игрока
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - 50, 40, 40)
        self.velocity = 0

    def jump(self):
        if self.rect.bottom >= HEIGHT:
            self.velocity = JUMP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)


# Класс препятствий (треугольные шипы)
class Obstacle:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT - 50
        self.size = 40

    def move(self):
        self.x -= SPEED

    def draw(self):
        points = [(self.x, self.y + self.size), (self.x + self.size // 2, self.y),
                  (self.x + self.size, self.y + self.size)]
        pygame.draw.polygon(screen, BLACK, points)


# Основной игровой цикл
def game_loop():
    player = Player()
    obstacles = [Obstacle(WIDTH + i * 300) for i in range(3)]
    clock = pygame.time.Clock()
    running = True
    game_over = False

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    game_loop()  # Перезапуск игры
                    return

        if not game_over:
            player.move()
            player.draw()

            for obstacle in obstacles:
                obstacle.move()
                obstacle.draw()
                if obstacle.x + obstacle.size < 0:
                    obstacle.x = WIDTH
                if player.rect.colliderect(pygame.Rect(obstacle.x, obstacle.y, obstacle.size, obstacle.size)):
                    game_over = True  # Конец игры при столкновении
        else:
            show_game_over()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


# Запуск игры
main_menu()
game_loop()