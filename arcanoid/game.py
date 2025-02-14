import pygame
import random
from ball import Ball
from paddle import Paddle
from brick import Brick


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = False
        self.ball = Ball(390, 300)
        self.paddle = Paddle(120, 10)
        self.bricks = [
            Brick(x * 80, y * 30 + 50, random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)]), random.choice([1, 2]))
            for x in range(10) for y in range(5)]
        self.balls = [self.ball]
        self.score = 0  # Инициализация счета
        self.double_brick_sound = None  # Звук для первого попадания в прочную стену
        self.hit_once = False  # Флаг для отслеживания первого попадания

        # Инициализация музыки и звуков
        try:
            pygame.mixer.init()
            pygame.mixer.music.load('background_music.mp3')
            pygame.mixer.music.set_volume(0.1)  # Уменьшение громкости фоновой музыки
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Background music error:", e)

        try:
            self.bounce_wall = pygame.mixer.Sound('brick.mp3')
            self.bounce_wall.set_volume(1.0)  # Максимальная громкость звука отскока от стен
            self.bounce_paddle = pygame.mixer.Sound('bounce.mp3')
            self.bounce_paddle.set_volume(1.0)  # Максимальная громкость звука отскока от платформы
            self.game_over_sound = pygame.mixer.Sound('gameover.mp3')  # Загрузка звука окончания игры
            self.game_over_sound.set_volume(1.0)  # Максимальная громкость звука окончания игры
            self.double_brick_sound = pygame.mixer.Sound('doublebrick.mp3')  # Звук для первого попадания
            self.double_brick_sound.set_volume(1.0)  # Максимальная громкость звука
            self.win_sound = pygame.mixer.Sound('win.mp3')  # Загрузка звука победы
            self.win_sound.set_volume(1.0)  # Максимальная громкость звука победы
        except Exception as e:
            print("Sound error:", e)

        try:
            self.background_image = pygame.image.load('background.png')
        except Exception as e:
            print("Background image error:", e)
            self.background_image = None

    def start_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to Start", True, (255, 255, 255))
        self.screen.blit(text, (400 - text.get_width() // 2, 300))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
        self.running = True

    def restart_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Game Over! Your Score: {self.score}. Press R to Restart", True, (255, 255, 255))
        self.screen.blit(text, (400 - text.get_width() // 2, 300))
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting = False
        self.__init__()

    def win_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("CONGRATULATIONS YOU WIN!", True, (255, 255, 255))
        score_text = font.render(f"Your Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (400 - text.get_width() // 2, 250))
        self.screen.blit(score_text, (400 - score_text.get_width() // 2, 300))
        pygame.display.flip()
        self.win_sound.play()  # Воспроизведение звука победы
        pygame.time.delay(3000)  # Задержка перед возвратом на стартовый экран
        self.start_screen()  # Возврат на начальный экран

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def update(self):
        keys = pygame.key.get_pressed()
        self.paddle.move(keys)
        for ball in self.balls:
            ball.move()
            # Проверка столкновения с платформой
            if ball.rect.colliderect(self.paddle.rect):
                ball.bounce_y()
                self.bounce_paddle.play()  # Воспроизведение звука отскока от платформы

            # Проверка столкновений с кирпичами
            for brick in self.bricks[:]:
                if ball.rect.colliderect(brick.rect):
                    ball.bounce_y()
                    if brick.hit():
                        self.bricks.remove(brick)
                        self.score += 100  # Увеличение счета на 100
                        if brick.health == 2:  # Если кирпич прочный
                            if not self.hit_once:
                                self.double_brick_sound.play()  # Воспроизведение звука для первого попадания
                                self.hit_once = True  # Устанавливаем флаг, чтобы звук не воспроизводился повторно
                        else:
                            self.bounce_wall.play()  # Воспроизведение звука отскока от кирпича

            # Проверка столкновений со стенами
            if ball.rect.left <= 0 or ball.rect.right >= 800:
                ball.bounce_x()
                self.bounce_wall.play()  # Воспроизведение звука отскока от стен

            # Проверка столкновения с верхней границей
            if ball.rect.top <= 0:
                ball.bounce_y()
                self.bounce_wall.play()  # Воспроизведение звука отскока от верхней границы

            # Проверка, если мяч упал ниже нижней границы
            if ball.rect.bottom >= 600:
                self.balls.remove(ball)
                if not self.balls:
                    self.game_over_sound.play()  # Воспроизведение звука окончания игры
                    self.running = False

        # Проверка на победу
        if not self.bricks:
            self.win_screen()

    def draw(self):
        if self.background_image:
            self.screen.blit(pygame.transform.scale(self.background_image, (800, 600)), (0, 0))
        else:
            self.screen.fill((0, 0, 0))

        # Рисуем ракетку
        pygame.draw.polygon(self.screen, (255, 0, 0), [
            (self.paddle.rect.left, self.paddle.rect.top),
            (self.paddle.rect.right, self.paddle.rect.top),
            (self.paddle.rect.right - 5, self.paddle.rect.bottom),
            (self.paddle.rect.left + 5, self.paddle.rect.bottom)
        ])
        pygame.draw.rect(self.screen, (200, 0, 0), self.paddle.rect.inflate(-10, 0))

        # Рисуем мячи
        for ball in self.balls:
            ball.draw(self.screen)

        # Рисуем кирпичи
        for brick in self.bricks:
            if brick.health == 2:
                pygame.draw.rect(self.screen, (169, 169, 169), brick.rect, 6)
            brick.draw(self.screen)

        # Отображаем счет
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self):
        self.start_screen()
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        self.restart_screen()

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()