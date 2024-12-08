import pygame
import random
from pathlib import Path

ROOT_DIR = str(Path(__file__).parent)
WIDTH, HEIGHT = 800, 600
FPS = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()


SPACESHIP_IMG = pygame.image.load(ROOT_DIR+"\\spaceship.png")  
SPACESHIP_IMG = pygame.transform.scale(SPACESHIP_IMG, (50, 50))
ENEMY_IMG = pygame.image.load(ROOT_DIR+"\\enemy.png")  
ENEMY_IMG = pygame.transform.scale(ENEMY_IMG, (50, 50))


class Spaceship:
    def __init__(self):
        self.image = SPACESHIP_IMG
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 60))
        self.speed = 5
        self.bullets = []

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.append(bullet)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(surface)

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)


class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x - 5, y, 10, 20)
        self.speed = -10

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

class Enemy:
    def __init__(self):
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect(
            center=(random.randint(0, WIDTH), random.randint(-100, -40))
        )
        self.speed = random.randint(3, 6)

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def main():
    running = True
    spaceship = Spaceship()
    enemies = [Enemy() for _ in range(5)]
    score = 0

    font = pygame.font.SysFont(None, 36)

    while running:
        screen.fill(WHITE)
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                spaceship.shoot()

        
        spaceship.move(keys)
        spaceship.update_bullets()

        for enemy in enemies[:]:
            enemy.move()
            if enemy.rect.top > HEIGHT:
                enemies.remove(enemy)
                enemies.append(Enemy())
            if enemy.rect.colliderect(spaceship.rect):
                print("Game Over!")
                running = False
            for bullet in spaceship.bullets:
                if enemy.rect.colliderect(bullet.rect):
                    spaceship.bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append(Enemy())
                    score += 1

        
        spaceship.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
