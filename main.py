import pygame
import sys
import random
from scoreboard import Scoreboard



pygame.init()
pygame.font.init()



font = pygame.font.Font(None, 36)
score_color = (50, 205, 50)


game_over_font = pygame.font.Font(None, 72)
game_over_color = (50, 205, 50)


button_color = (170, 255, 0)
hover_color = (9, 121, 105)
font_color = (255, 255, 255)


retry_button_rect = pygame.Rect(200, 350, 200, 50)
exit_button_rect = pygame.Rect(400, 350, 200, 50)

retry_button_color = button_color
exit_button_color = button_color



WIDTH, HEIGHT = 800, 600
BG_COLOR = (0, 0, 0)
IMAGE_WIDTH, IMAGE_HEIGHT = 100, 100
LASER_IMG = pygame.image.load("assets/img/laser.png")
LASER_IMG = pygame.transform.scale(LASER_IMG, (10, 30))
ALIEN_IMG = pygame.image.load("assets/img/alien.png")
ALIEN_IMG = pygame.transform.scale(ALIEN_IMG, (100, 100))

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Player's spaceship
player_img = pygame.image.load("assets/img/rocket.png")
player_img = pygame.transform.scale(player_img, (100, 100))
player_x = (WIDTH - IMAGE_WIDTH) // 2
player_y = 450
player_x_speed = 0

# Player control settings
player_speed = 4.5
lasers = []

scoreboard = Scoreboard()

class Laser:
    def __init__(self, x, y):
        self.x = x + IMAGE_WIDTH // 2 - 5
        self.y = y
        self.state = "fire"

# Alien properties
num_aliens = 5
aliens = []

for _ in range(num_aliens):
    alien_x = random.randint(0, WIDTH - IMAGE_WIDTH)
    alien_y = random.randint(-500, -100)
    alien_x_speed = random.choice([-2, 2])
    aliens.append({"x": alien_x, "y": alien_y, "speed": alien_x_speed})


# Function to check for collisions
def is_collision(laser, alien):
    laser_rect = pygame.Rect(laser.x, laser.y, 10, 30)
    alien_rect = pygame.Rect(alien["x"], alien["y"], 100, 100)
    return laser_rect.colliderect(alien_rect)


def spawn_alien():
    alien_x = random.randint(0, WIDTH - IMAGE_WIDTH)
    alien_y = random.randint(-500, -100)
    alien_x_speed = random.choice([-2, 2])
    aliens.append({"x": alien_x, "y": alien_y, "speed": alien_x_speed})


game_over = False


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_speed = -player_speed
            if event.key == pygame.K_RIGHT:
                player_x_speed = player_speed
            if event.key == pygame.K_SPACE:
                lasers.append(Laser(player_x, player_y))

        # Check for key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_speed = 0

    # Update the player's position
    player_x += player_x_speed

    # Boundaries for the player's spaceship
    if player_x < 0:
        player_x = 0
    elif player_x > WIDTH - IMAGE_WIDTH:
        player_x = WIDTH - IMAGE_WIDTH


    screen.fill(BG_COLOR)

    # Check if an alien touches the rocket or goes past it
    for alien in aliens:
        if (
            player_x < alien["x"] + IMAGE_WIDTH
            and player_x + IMAGE_WIDTH > alien["x"]
            and player_y < alien["y"] + IMAGE_HEIGHT
            and player_y + IMAGE_HEIGHT > alien["y"]
        ):
            game_over = True

        if alien["y"] > HEIGHT:
            aliens.remove(alien)
            scoreboard.lose_point(1)


    # Check for collisions between lasers and aliens
    for laser in lasers:
        for alien in aliens:
            if laser.state == "fire" and is_collision(laser, alien):
                lasers.remove(laser)
                aliens.remove(alien)
                scoreboard.gain_point(3)



    if not aliens:
        for _ in range(num_aliens):
            spawn_alien()


    # Move and draw lasers
    for laser in lasers:
        if laser.state == "fire":
            laser.y -= 8
            if laser.y < 0:
                laser.state = "ready"
            else:
                screen.blit(LASER_IMG, (laser.x, laser.y))


    # Move and draw aliens
    for alien in aliens:
        alien["y"] += 1
        if alien["y"] > HEIGHT:
            alien["y"] = random.randint(-500, -100)
            alien["x"] = random.randint(0, WIDTH - IMAGE_WIDTH)
        screen.blit(ALIEN_IMG, (alien["x"], alien["y"]))


    screen.blit(player_img, (player_x, player_y))


    score_text = font.render(f"Score: {scoreboard.score}", True, score_color)
    screen.blit(score_text, (10, 10))


    if game_over:
        game_over_text = game_over_font.render("Game Over", True, game_over_color)
        screen.blit(game_over_text,
                    ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))

    # After the game-over loop
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.MOUSEMOTION:
                if retry_button_rect.collidepoint(event.pos):
                    retry_button_color = hover_color
                else:
                    retry_button_color = button_color
                if exit_button_rect.collidepoint(event.pos):
                    exit_button_color = hover_color
                else:
                    exit_button_color = button_color
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    game_over = False
                    scoreboard.score = 0
                    player_x = (WIDTH - IMAGE_WIDTH) // 2
                    player_y = 450
                    aliens.clear()
                    lasers.clear()
                elif exit_button_rect.collidepoint(event.pos):

                    pygame.quit()
                    sys.exit()

        # Clear the screen
        screen.fill(BG_COLOR)

        # Display "Game Over" message and score
        game_over_text = game_over_font.render("Game Over", True, game_over_color)
        screen.blit(game_over_text,
                    ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))

        score_text = font.render(f"Score: {scoreboard.score}", True, score_color)
        screen.blit(score_text, (10, 10))

        # Draw "Retry" and "Exit" buttons
        pygame.draw.rect(screen, retry_button_color, retry_button_rect)
        pygame.draw.rect(screen, exit_button_color, exit_button_rect)

        # Draw text on buttons
        retry_text = font.render("Retry", True, font_color)
        exit_text = font.render("Exit", True, font_color)
        screen.blit(retry_text, ((retry_button_rect.centerx - retry_text.get_width() // 2),
                                 retry_button_rect.centery - retry_text.get_height() // 2))
        screen.blit(exit_text, ((exit_button_rect.centerx - exit_text.get_width() // 2),
                                exit_button_rect.centery - exit_text.get_height() // 2))




    pygame.display.update()

    # Check game-over state
    if game_over:
        running = False



print("Game Over")


pygame.quit()
sys.exit()