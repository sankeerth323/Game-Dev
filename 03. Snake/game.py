import pygame
import random
import os

ASSET_PATH = os.path.join("assets", "Graphics")
pygame.init()
font = pygame.font.Font(None, 36)

sw, sh = 700, 700
screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
BLOCK_SIZE = 20

running = True
game_over = False
move_delay = 150
move_timer = 0

snake_list = [(360, 340), (340, 340), (320, 340)]
current_direction = 'RIGHT'
move_direction = 'RIGHT'
food_rect = None

sprites = {
    "head": {
        "up": pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "head_up.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        "down": pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "head_down.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        "left": pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "head_left.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        "right": pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "head_right.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        )
    },

    "tail": {
        "up": pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "tail_up.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        "down": pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "tail_down.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        "left": pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "tail_left.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        "right": pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "tail_right.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        )
    },

    "bodies": {
        "horizontal": pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "body_horizontal.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        "vertical": pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "body_vertical.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        )
    },

    "corners": {
        ("up", "right"): pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "body_topright.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        ("right", "up"): pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "body_topright.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),

        ("up", "left"): pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "body_topleft.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        ("left", "up"): pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "body_topleft.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),

        ("down", "right"): pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "body_bottomright.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        ("right", "down"): pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "body_bottomright.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),

        ("down", "left"): pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "body_bottomleft.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
        ("left", "down"): pygame.transform.scale(
            pygame.image.load(os.path.join(ASSET_PATH, "body_bottomleft.png")).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE)
        ),
    },

    "apple": pygame.transform.scale(
        pygame.image.load(os.path.join(ASSET_PATH, "apple.png")).convert_alpha(),(BLOCK_SIZE, BLOCK_SIZE)
    )
}

dir_map = {
    (0, -BLOCK_SIZE) : 'up',
    (0, BLOCK_SIZE) : 'down',
    (BLOCK_SIZE, 0) : 'right',
    (-BLOCK_SIZE, 0) : 'left'
}

opposite = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left"
}


def reset_game():
    global snake_list, current_direction, move_direction
    global food_rect, game_over, move_timer

    snake_list = [(360, 340), (340, 340), (320, 340)]
    current_direction = 'RIGHT'
    move_direction = 'RIGHT'
    food_rect = None
    move_timer = 0
    game_over = False


while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    if not game_over:
        if not food_rect:
            while True:
                food_row = random.randint(1, 33)
                food_col = random.randint(1, 33)

                valid = True
                for b in snake_list:
                    if food_row * BLOCK_SIZE == b[0] and food_col * BLOCK_SIZE == b[1]:
                        valid = False
                        break

                if valid:
                    food_rect = pygame.Rect(food_row * BLOCK_SIZE, food_col * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            current_direction = 'UP'
        elif keys[pygame.K_s]:
            current_direction = 'DOWN'
        elif keys[pygame.K_a]:
            current_direction = 'LEFT'
        elif keys[pygame.K_d]:
            current_direction = 'RIGHT'

        move_timer += dt
        if move_timer >= move_delay:
            move_timer -= move_delay

            if current_direction == 'UP' and move_direction != 'DOWN':
                move_direction = 'UP'
            elif current_direction == 'DOWN' and move_direction != 'UP':
                move_direction = 'DOWN'
            elif current_direction == 'LEFT' and move_direction != 'RIGHT':
                move_direction = 'LEFT'
            elif current_direction == 'RIGHT' and move_direction != 'LEFT':
                move_direction = 'RIGHT'

            head_x, head_y = snake_list[0]

            if move_direction == 'UP':
                new_head = (head_x, head_y - BLOCK_SIZE)
            elif move_direction == 'DOWN':
                new_head = (head_x, head_y + BLOCK_SIZE)
            elif move_direction == 'LEFT':
                new_head = (head_x - BLOCK_SIZE, head_y)
            elif move_direction == 'RIGHT':
                new_head = (head_x + BLOCK_SIZE, head_y)

            if (
                new_head[0] < BLOCK_SIZE or
                new_head[0] > sw - 2 * BLOCK_SIZE or
                new_head[1] < BLOCK_SIZE or
                new_head[1] > sh - 2 * BLOCK_SIZE
            ):
                game_over = True
            else:
                snake_list.insert(0, new_head)

                if new_head in snake_list[1:]:
                    game_over = True
                else:
                    if food_rect and new_head == (food_rect.x, food_rect.y):
                        food_rect = None
                    else:
                        snake_list.pop()

    screen.fill(pygame.Color('Black'))

    for i in range(0, 36):
        pygame.draw.rect(screen, pygame.Color('brown'), (0, i * 20, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, pygame.Color('brown'), (sw - 20, i * 20, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, pygame.Color('brown'), (i * 20, 0, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, pygame.Color('brown'), (i * 20, sh - 20, BLOCK_SIZE, BLOCK_SIZE))

    screen.blit(sprites["head"][move_direction.lower()],(snake_list[0][0],snake_list[0][1]))
    
    for i in range(1,len(snake_list) - 1):
        prev = snake_list[i-1]
        curr = snake_list[i]
        next = snake_list[i+1]

        dx1 = prev[0] - curr[0]
        dy1= prev[1] - curr[1]
        dir1 = dir_map[(dx1,dy1)]

        dx2 = next[0] - curr[0]
        dy2 = next[1] - curr[1]
        dir2 = dir_map[(dx2,dy2)]

        is_straight = opposite[dir1] == dir2
        axis = "horizontal" if dir1 in ("left", "right") else "vertical"

        if is_straight:
            screen.blit(sprites["bodies"][axis],(curr[0],curr[1]))
        else:
            screen.blit(sprites["corners"][(dir1,dir2)],(curr[0],curr[1]))

    tail = snake_list[-1]
    before_tail = snake_list[-2]
    if before_tail[0] < tail[0]:
        screen.blit(sprites["tail"]["right"],(tail[0],tail[1]))
    elif before_tail[0] > tail[0]:
        screen.blit(sprites["tail"]["left"],(tail[0],tail[1]))
    elif before_tail[1] < tail[1]:
        screen.blit(sprites["tail"]["down"],(tail[0],tail[1]))
    elif before_tail[1] > tail[1]:
        screen.blit(sprites["tail"]["up"],(tail[0],tail[1]))
    
    tail = snake_list[-1]
    before_tail = snake_list[-2]

    if food_rect:
        screen.blit(sprites["apple"], (food_rect.x, food_rect.y))

    score = len(snake_list) - 3
    score_surface = font.render(f"Score: {score}", True, pygame.Color('white'))
    screen.blit(score_surface, (30, 30))

    if game_over:
        over_surface = font.render("GAME OVER - Press R to Restart", True, pygame.Color('red'))
        screen.blit(over_surface, (sw // 2 - over_surface.get_width() // 2, sh // 2))

    pygame.display.update()

pygame.quit()