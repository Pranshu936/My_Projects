import pygame
import random

# Initialize pygame and its sound module
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load sound effects
hit_sound = pygame.mixer.Sound("hit.wav")
lose_life_sound = pygame.mixer.Sound("lose_life.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
powerup_sound = pygame.mixer.Sound("powerup.wav")

# Font for text display
font = pygame.font.Font(None, 36)

# Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([80, 10])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH // 2) - 40
        self.rect.y = SCREEN_HEIGHT - 20
        self.speed_x = 0
        self.is_enlarged = False
        self.enlarged_timer = 0

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

        # Power-up timer for enlarged paddle
        if self.is_enlarged:
            self.enlarged_timer -= 1
            if self.enlarged_timer <= 0:
                self.image = pygame.Surface([80, 10])
                self.image.fill(GREEN)
                self.is_enlarged = False

# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([-2, 2])
        self.speed_y = -2

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - 10:
            self.speed_x = -self.speed_x
        if self.rect.y <= 0:
            self.speed_y = -self.speed_y
        if self.rect.y >= SCREEN_HEIGHT:
            return True  # Return True if the ball goes past the paddle
        return False

# Block class
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([50, 20])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_y = 3

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()  # Remove the power-up if it goes off the screen

# Game setup
def main():
    pygame.display.set_caption('Block Breaker')

    # Create paddle, ball, and sprite groups
    paddle = Paddle()
    ball = Ball()

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    all_sprites.add(paddle)
    all_sprites.add(ball)

    # Function to create blocks
    def create_blocks():
        for row in range(5):
            for col in range(11):
                block = Block(col * 55 + 5, row * 25 + 80)
                all_sprites.add(block)
                blocks.add(block)

    create_blocks()

    # Game variables
    running = True
    clock = pygame.time.Clock()
    lives = 3
    score = 0
    level = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Get the current mouse position
            mouse_x, _ = pygame.mouse.get_pos()

            # Set the paddle's x-coordinate to follow the mouse's x-coordinate
            paddle.rect.x = mouse_x - paddle.rect.width // 2

            # Prevent the paddle from moving off-screen
            if paddle.rect.x < 0:
                paddle.rect.x = 0
            if paddle.rect.x > SCREEN_WIDTH - paddle.rect.width:
                paddle.rect.x = SCREEN_WIDTH - paddle.rect.width

        all_sprites.update()

        # Ball and paddle collision
        if pygame.sprite.collide_rect(ball, paddle):
            ball.speed_y = -ball.speed_y
            hit_sound.play()

        # Ball and block collision
        block_hit_list = pygame.sprite.spritecollide(ball, blocks, True)
        if block_hit_list:
            ball.speed_y = -ball.speed_y
            hit_sound.play()
            score += 10 * len(block_hit_list)

            # Randomly generate power-ups
            if random.random() < 0.1:
                powerup = PowerUp(ball.rect.x, ball.rect.y)
                all_sprites.add(powerup)
                powerups.add(powerup)

        # Power-up and paddle collision
        powerup_hit_list = pygame.sprite.spritecollide(paddle, powerups, True)
        for powerup in powerup_hit_list:
            powerup_sound.play()
            paddle.image = pygame.Surface([160, 10])
            paddle.image.fill(GREEN)
            paddle.is_enlarged = True
            paddle.enlarged_timer = 500

        # Check if all blocks are destroyed (level up)
        if len(blocks) == 0:
            level += 1
            ball.speed_x += 1  # Increase difficulty
            ball.speed_y += 1
            create_blocks()

        # Check if ball goes past the paddle (lose life)
        if ball.update():
            lives -= 1
            lose_life_sound.play()
            if lives == 0:
                game_over_sound.play()
                running = False  # End game if no lives are left
            else:
                # Reset ball position and speed after losing a life
                ball.rect.x = SCREEN_WIDTH // 2
                ball.rect.y = SCREEN_HEIGHT // 2
                ball.speed_x = random.choice([-2, 2])
                ball.speed_y = -2

        # Clear the screen
        screen.fill(BLACK)

        # Draw all sprites
        all_sprites.draw(screen)

        # Display score, lives, and level
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 40, 10))

        # Update the screen
        pygame.display.flip()

        # Limit frame rate
        clock.tick(60)

    # Game Over screen
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, RED)
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before quitting

    pygame.quit()

if __name__ == "__main__":
    main()
