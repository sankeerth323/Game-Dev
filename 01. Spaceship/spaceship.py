import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Side Scrolling Platformer with Bullets")

# Colors
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

# Game settings
fps = 60
clock = pygame.time.Clock()

# Player settings
player_size = 40
player_x = 100
player_y = height - player_size
player_speed = 5
gravity = 0.5
jump_power = 12
player_velocity_y = 0
on_ground = True

# Platform settings
platform_width = 100
platform_height = 10
platform_speed = 5
platform_list = [[100, height - 50], [300, height - 150], [600, height - 250]]

# Bullet settings
bullet_width = 20
bullet_height = 20
bullet_speed = 7
bullet_list = []
bullet_spawn_delay = 100  # Frames before the first bullet spawns
bullet_frequency = 50    # Spawn bullets every X frames


def draw_player(x, y):
    """Draw the player."""
    pygame.draw.rect(screen, blue, [x, y, player_size, player_size])


def draw_platforms(platforms):
    """Draw the platforms."""
    for platform in platforms:
        pygame.draw.rect(screen, green, [platform[0], platform[1], platform_width, platform_height])


def draw_bullets(bullets):
    """Draw the bullets."""
    for bullet in bullets:
        pygame.draw.rect(screen, red, [bullet[0], bullet[1], bullet_width, bullet_height])


def check_collision(x, y, platforms):
    """Check if the player is landing on a platform."""
    for platform in platforms:
        if (
            y + player_size >= platform[1]
            and y + player_size <= platform[1] + platform_height
            and x + player_size > platform[0]
            and x < platform[0] + platform_width
        ):
            return platform
    return None


def check_bullet_collision(x, y, bullets):
    """Check if the player touches a bullet."""
    for bullet in bullets:
        if (
            x < bullet[0] + bullet_width
            and x + player_size > bullet[0]
            and y < bullet[1] + bullet_height
            and y + player_size > bullet[1]
        ):
            return True
    return False


def game_loop():
    global player_x, player_y, player_velocity_y, on_ground, bullet_list

    # Game variables
    game_over = False
    score = 0
    frame_count = 0

    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Get key presses
        keys = pygame.key.get_pressed()
        player_x_change = 0

        if keys[pygame.K_LEFT]:
            player_x_change = -player_speed
        elif keys[pygame.K_RIGHT]:
            player_x_change = player_speed

        # Jumping
        if keys[pygame.K_SPACE] and on_ground:
            player_velocity_y = -jump_power
            on_ground = False

        # Apply movement
        player_x += player_x_change
        player_y += player_velocity_y
        player_velocity_y += gravity

        # Prevent player from going off-screen horizontally
        if player_x < 0:
            player_x = 0
        elif player_x > width - player_size:
            player_x = width - player_size

        # Move platforms to create scrolling effect
        for platform in platform_list:
            platform[0] -= platform_speed

        # Generate new platforms when old ones move out
        if platform_list[0][0] < -platform_width:
            platform_list.pop(0)
            new_platform_y = random.randint(height - 250, height - 50)
            platform_list.append([width, new_platform_y])
            score += 1

        # Spawn bullets randomly after initial delay
        frame_count += 1
        if frame_count > bullet_spawn_delay and frame_count % bullet_frequency == 0:
            bullet_y = random.randint(0, height - bullet_height)
            bullet_list.append([width, bullet_y])

        # Move bullets from right to left
        for bullet in bullet_list:
            bullet[0] -= bullet_speed

        # Remove bullets that move off-screen
        bullet_list = [bullet for bullet in bullet_list if bullet[0] > -bullet_width]

        # Check for collisions with platforms
        platform_collision = check_collision(player_x, player_y, platform_list)

        # Platform collision logic
        if platform_collision and player_velocity_y >= 0:
            player_y = platform_collision[1] - player_size
            player_velocity_y = 0
            on_ground = True
        elif player_y + player_size >= height:  # Hit the bottom of the screen
            player_y = height - player_size
            player_velocity_y = 0
            on_ground = True
        else:
            on_ground = False

        # Prevent player from falling below the screen
        if player_y > height - player_size:
            player_y = height - player_size
            player_velocity_y = 0
            on_ground = True

        # Check for collision with bullets after initial delay
        if frame_count > bullet_spawn_delay and check_bullet_collision(player_x, player_y, bullet_list):
            print("Game Over! You hit a bullet.")
            game_over = True

        # Drawing section
        screen.fill(black)
        draw_player(player_x, player_y)
        draw_platforms(platform_list)
        draw_bullets(bullet_list)

        # Display score
        font = pygame.font.SysFont("comicsansms", 25)
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, [10, 10])

        # Update the display
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


# Run the game
game_loop()
