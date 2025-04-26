import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
GRAVITY = 0.5
JUMP_STRENGTH = -10
SPEED = 6
WIN_SCORE = 25
OBSTACLE_SPACING = 300

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash")

font = pygame.font.Font(None, 50)

menu_image = pygame.image.load("menu.png").convert_alpha()
menu_image = pygame.transform.smoothscale(menu_image, (WIDTH, HEIGHT))
background_image = pygame.image.load("fon.png").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
player_image = pygame.image.load("kyb.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (40, 40))
end_background = pygame.image.load("").convert()
end_background = pygame.transform.scale(end_background, (WIDTH, HEIGHT))

def main_menu():
    while True:
        screen.blit(menu_image, (0, 0))
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

def show_end_screen(message):
    screen.blit(end_background, (0, 0))
    text_surface = font.render(message, True, WHITE)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 50))
    pygame.draw.polygon(screen, (0, 255, 0), [(375, 250), (425, 250), (400, 300)])
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 375 < x < 425 and 250 < y < 300:
                    waiting = False

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
        screen.blit(player_image, self.rect.topleft)

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

def game_loop():
    player = Player()
    obstacles = [Obstacle(WIDTH + i * OBSTACLE_SPACING, random.choice([1, 2, 3])) for i in range(6)]
    clock = pygame.time.Clock()
    running = True
    game_over = False
    win = False
    score = 0

    while running:
        if not game_over and not win:
            screen.blit(background_image, (0, 0))
        else:
            screen.blit(end_background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and (game_over or win):
                x, y = pygame.mouse.get_pos()
                if 375 < x < 425 and 250 < y < 300:
                    game_loop()
                    return
            if event.type == pygame.KEYDOWN and not game_over and not win:
                if event.key == pygame.K_SPACE:
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

            score_text = font.render(f"Пройдено: {score}/{WIN_SCORE}", True, BLACK)
            screen.blit(score_text, (10, 10))

            if score >= WIN_SCORE:
                win = True
        elif game_over:
            show_end_screen("Ты проиграл!")
            return
        elif win:
            show_end_screen("Ты выиграл!")
            return

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

main_menu()
game_loop()
