import pygame
from random import uniform
pygame.init()
pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load('assets/sounds/intro.ogg')
p1_sfx = pygame.mixer.Sound('assets/sounds/p1.wav')
p2_sfx = pygame.mixer.Sound('assets/sounds/p2.wav')
bounce = pygame.mixer.Sound('assets/sounds/bounce.wav')
font = pygame.font.SysFont(None,36)
score1,score2 = 0,0
sw = 900
sh = 700

INTRO_DURATION = 8.0
intro_time = 0
game_started = False
waiting = True
wait_timer = 0
WAIT_TIME = 0.5

screen = pygame.display.set_mode((sw, sh))
screen_rect = screen.get_rect()
pygame.display.set_caption("Jabbu Pong")
clock = pygame.time.Clock()
running = True

left_paddle_area = pygame.Rect(0,0,screen.get_width()//2 - 150,screen.get_height())
right_paddle_area = pygame.Rect(screen.get_width()//2 + 150,0,screen.get_width()//2,screen.get_height())
divider_line = pygame.Rect(screen.get_width()//2,0,3,screen.get_height())
p1_score = font.render((f"Player 1:  {score1}"),True,pygame.Color('white'),None)
p2_score = font.render((f"Player 2:  {score2}"),True,pygame.Color('white'),None)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 100)
        self.speed = 450

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.rect.y += self.speed * dt

        self.rect.clamp_ip(left_paddle_area)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color("white"), self.rect)
    
    def reset(self):
        self.rect.center = (50,screen.get_height()//2 - 50)

class Player2:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 100)
        self.speed = 400

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed * dt

        self.rect.clamp_ip(right_paddle_area)
    
    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color("white"), self.rect)
    
    def reset(self):
        self.rect.center = (sw-50, screen.get_height()//2 - 50)

class Ball:
    def __init__(self, x, y):
        original = pygame.image.load("assets/img/jfinal.jpeg").convert_alpha()
        self.original_image = pygame.transform.smoothscale(original, (40, 40))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 650
        self.yspeed = 100
        self.angle = 0
        self.rotation_speed = 360

    def update(self, dt):
        self.rect.x += self.speed * dt
        self.rect.y += self.yspeed * dt
        self.angle = (self.angle + self.rotation_speed * dt) % 360
        center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=center)

    def reset(self,center,direction):
        self.rect.center = center
        self.speed = direction * abs(self.speed)
        self.yspeed = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

player = Player(50,screen.get_height()//2 - 50)
player2 = Player2(sw-50, screen.get_height()//2 - 50)
ball = Ball(screen.get_width()//2,screen.get_height()//2)
paddles = [player,player2]

def reset_round(scoring_player, serve_direction):
    global waiting, wait_timer, score1, score2

    if scoring_player == 1:
        score1 += 1
    else:
        score2 += 1

    ball.reset(screen_rect.center, serve_direction)
    player.reset()
    player2.reset()

    waiting = True
    wait_timer = 0

pygame.mixer.music.play()

while running:
    dt = clock.tick(60) / 1000

    if not game_started:
        intro_time += dt
        if intro_time >= INTRO_DURATION:
            game_started = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not waiting and game_started:
        player.update(dt)
        player2.update(dt)
        ball.update(dt)

    hit_paddle = None
    if ball.rect.colliderect(player.rect) and ball.speed < 0:
            hit_paddle = player            
    elif ball.rect.colliderect(player2.rect) and ball.speed > 0:
            hit_paddle = player2
    
    if hit_paddle:
        if ball.speed > 0:
            ball.rect.right = hit_paddle.rect.left
            p2_sfx.play()
        elif ball.speed < 0:
            ball.rect.left = hit_paddle.rect.right
            p1_sfx.play()
        offset = ball.rect.centery - hit_paddle.rect.centery
        half_paddle = hit_paddle.rect.height / 2
        normalized = offset / half_paddle
        normalized = max(-1, min(1, normalized))
        CENTER_ZONE = 0.15
        if abs(normalized) <= CENTER_ZONE:
            normalized = uniform(-0.6, 0.6)
        ball.yspeed = normalized * abs(ball.speed)
        ball.speed *= -1    

    if not waiting:
        if ball.rect.left < screen_rect.left:
            reset_round(scoring_player=2, serve_direction=1)
            p2_score = font.render((f"Player 2:  {score2}"),True,pygame.Color('white'),None)

        elif ball.rect.right > screen_rect.right:
            reset_round(scoring_player=1, serve_direction=-1)
            p1_score = font.render((f"Player 1:  {score1}"),True,pygame.Color('white'),None)

    if waiting:
        wait_timer += dt
        if wait_timer >= WAIT_TIME:
            waiting = False
            wait_timer = 0

    if ball.rect.bottom >= screen_rect.bottom:
        ball.yspeed *= -1
        bounce.play()
    if ball.rect.top <= screen_rect.top:
        ball.yspeed *= -1
        bounce.play()

    screen.fill(pygame.Color("black"))
    pygame.draw.rect(screen,pygame.Color('white'),divider_line)
    player.draw(screen)
    player2.draw(screen)
    ball.draw(screen)
    screen.blit(p1_score,(20,20))
    screen.blit(p2_score,(750,20))
    pygame.display.flip()

pygame.quit()