# Імпортуємо необхідні бібліотеки
import pygame
import sys
import random

# Ініціалізація Pygame
pygame.init()
pygame.mixer.init()

# Завантаження музики
try:
    pygame.mixer.music.load("chiptune_sherlock_holmes_anthem-2152252.mp3")
    pygame.mixer.music.play(-1)  # Безкінечне повторення
except Exception as e:
    print("Не вдалося завантажити музику:", e)

# Розміри вікна
WIDTH, HEIGHT = 800, 400
GRAVITY = 0.5
JUMP_STRENGTH = -10
SPEED = 6
WIN_SCORE = 25
OBSTACLE_SPACING = 300

# Кольори
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Створення екрану
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash")

# Шрифт
font = pygame.font.Font(None, 50)

# Завантаження зображень
menu_image = pygame.image.load("menu.png").convert_alpha()
menu_image = pygame.transform.smoothscale(menu_image, (WIDTH, HEIGHT))
background_image = pygame.image.load("fon.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
player_image = pygame.image.load("kub.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (80, 60))

# Статистика гравця
stats = {
    "jumps": 0,
    "deaths": 0,
    "wins": 0
}

# Клас порталу
class Portal:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT - 90, 40, 80)

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=10)

# Головне меню

def main_menu():
    while True:
        screen.blit(menu_image, (0, 0))

        stats_text = [
            font.render(str(stats['jumps']), True, BLACK),
            font.render(str(stats['deaths']), True, BLACK),
            font.render(str(stats['wins']), True, BLACK)
        ]

        for i, line in enumerate(stats_text):
            screen.blit(line, (WIDTH - 60, 50 + i * 30))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 350 < x < 450 and 40 < y < 140:
                    return
                elif 350 < x < 450 and 260 < y < 360:
                    pygame.quit()
                    sys.exit()

# Екран завершення гри

def show_end_screen(message):
    screen.fill(WHITE)
    text_surface = font.render(message, True, BLACK)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 100))

    restart_button = pygame.Rect(250, 250, 120, 50)
    menu_button = pygame.Rect(450, 250, 120, 50)

    pygame.draw.rect(screen, (0, 255, 0), restart_button, border_radius=10)
    pygame.draw.rect(screen, (255, 0, 0), menu_button, border_radius=10)

    restart_text = font.render("Рестарт", True, BLACK)
    screen.blit(restart_text, (restart_button.centerx - restart_text.get_width() // 2,
                               restart_button.centery - restart_text.get_height() // 2))

    menu_text = font.render("Меню", True, BLACK)
    screen.blit(menu_text, (menu_button.centerx - menu_text.get_width() // 2,
                             menu_button.centery - menu_text.get_height() // 2))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if restart_button.collidepoint(x, y):
                    return "restart"
                elif menu_button.collidepoint(x, y):
                    return "menu"

# Клас гравця
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT - 50, 40, 40)
        self.velocity = 0

    def jump(self):
        if self.rect.bottom >= HEIGHT:
            self.velocity = JUMP_STRENGTH
            stats["jumps"] += 1

    def move(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self):
        screen.blit(player_image, self.rect.topleft)

# Клас перешкод
class Obstacle:
    def __init__(self, x, variant):
        self.rect = pygame.Rect(x, HEIGHT - 50, 40, 40)
        self.passed = False
        self.variant = variant

    def move(self):
        self.rect.x -= SPEED

    def draw(self):
        if self.variant == 1:
            points = [
                (self.rect.left, self.rect.bottom),
                (self.rect.centerx, self.rect.top - 10),
                (self.rect.right, self.rect.bottom)
            ]
        elif self.variant == 2:
            points = [
                (self.rect.left, self.rect.bottom),
                (self.rect.centerx, self.rect.top - 20),
                (self.rect.right, self.rect.bottom)
            ]
        else:
            points = [
                (self.rect.left, self.rect.bottom),
                (self.rect.centerx, self.rect.top),
                (self.rect.right, self.rect.bottom)
            ]
        pygame.draw.polygon(screen, BLACK, points)

# Другий рівень

def level_two():
    global SPEED
    SPEED = 8
    game_loop(level=2)

# Ігровий цикл

def game_loop(level=1):
    global SPEED
    SPEED = 6 if level == 1 else 7
    player = Player()
    obstacles = [Obstacle(WIDTH + i * OBSTACLE_SPACING, random.choice([1, 2, 3])) for i in range(6)]
    portal = Portal(WIDTH + OBSTACLE_SPACING * 24 + 300)
    clock = pygame.time.Clock()
    running = True
    game_over = False
    win = False
    score = 0

    while running:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over and not win:
                    player.jump()

        if not game_over and not win:
            player.move()
            player.draw()

            for i, obstacle in enumerate(obstacles):
                obstacle.move()
                obstacle.draw()
                if obstacle.rect.right < 0:
                    new_x = max(ob.rect.right for ob in obstacles) + OBSTACLE_SPACING
                    obstacles[i] = Obstacle(new_x, random.choice([1, 2, 3]))

                if not obstacle.passed and obstacle.rect.right < player.rect.left:
                    obstacle.passed = True
                    score += 1

                if player.rect.colliderect(obstacle.rect):
                    game_over = True
                    stats["deaths"] += 1

            portal.draw()
            portal.rect.x -= SPEED

            if player.rect.colliderect(portal.rect):
                level_two()
                return

            score_text = font.render(f"Перешкод пройдено: {score} з {WIN_SCORE}", True, BLACK)
            screen.blit(score_text, (10, 10))

            if score >= WIN_SCORE:
                win = True
                stats["wins"] += 1

        else:
            if game_over:
                result = show_end_screen("Ти програв!")
            elif win:
                result = show_end_screen("Ти виграв!")

            if result == "restart":
                game_loop(level=1)
            elif result == "menu":
                main_menu()
            return

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Запуск гри
main_menu()
game_loop()

# хештеги: #гра #платформер #рівні #музика #чіптюн #GeometryDash
