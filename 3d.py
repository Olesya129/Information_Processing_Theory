import pygame
import random
import math
import asyncio
import platform

# Экран
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
BLACK = (10, 10, 20)
COLORS = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255), (128, 0, 255)]

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks")
clock = pygame.time.Clock()

# Частица
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 6)
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.life = 100
        self.color = color
        self.size = random.randint(1, 1)  # Размер частиц увеличен

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.05  # Гравитация
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = max(0, min(255, int(255 * (self.life / 100))))
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

# Взрыв
class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.target_y = random.randint(100, HEIGHT // 2)
        self.color = random.choice(COLORS)
        self.vel_y = -random.uniform(4, 7)
        self.exploded = False
        self.particles = []

    def update(self):
        if not self.exploded:
            self.y += self.vel_y
            if self.y <= self.target_y:
                self.exploded = True
                for _ in range(100):
                    self.particles.append(Particle(self.x, self.y, self.color))
        else:
            for p in self.particles:
                p.update()
            self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)
        else:
            for p in self.particles:
                p.draw(surface)

fireworks = []

async def main():
    while True:
        screen.fill(BLACK)

        if random.random() < 0.02:
            fireworks.append(Firework())

        for f in fireworks:
            f.update()
            f.draw(screen)

        fireworks[:] = [f for f in fireworks if not (f.exploded and not f.particles)]

        pygame.display.flip()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())


# Окно 1: Визуализация первых 5 изображений (истинные метки и предсказания)
# plt.figure(figsize=(15, 6))

# # Первый ряд: Истинные метки
# for i in range(5):
#     plt.subplot(2, 10, i + 1)
#     plt.imshow(X_test[i].reshape(28, 28), cmap='gray')
#     plt.title(f'Истинная: {y_test[i]}')
#     plt.axis('off')
#
# # Второй ряд: Предсказания
# for i in range(5):
#     plt.subplot(2, 10, i + 6)
#     plt.imshow(X_test[i].reshape(28, 28), cmap='gray')
#     plt.title(f'Предсказание: {y_pred[i]}')
#     plt.axis('off')

# plt.tight_layout()
# plt.show()