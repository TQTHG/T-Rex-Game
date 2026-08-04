import pygame

pygame.init()

# Screen
width = 1200
height = 800

# Frame Per Second
fps = 60
clock = pygame.time.Clock()

# Color
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)

# Font
font = pygame.font.SysFont(None,30)

# Score
score = 0
best_score = 0

# Ground
ground_y = height - 100
ground_rect = pygame.Rect(0 , ground_y , width , height)

# Speed
frame_count = 0

# T-Rex
trex_width = 40
trex_height = 60

trex_x =  int(width * 1/5)
trex_y =  ground_y - trex_height - 500

trex_rect = pygame.Rect(trex_x,trex_y,trex_width,trex_height)

# Physics
gravity = 1
vy_trex = 0

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("")

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    frame_count += 1
    if frame_count >= fps // 12:
        score += 1
        frame_count = 0

    vy_trex += gravity
    trex_y += vy_trex

    if trex_y  >= ground_y - trex_height:
        vy_trex = 0
        trex_y = ground_y - trex_height

    trex_rect = pygame.Rect(trex_x,trex_y,trex_width,trex_height)

    ground = pygame.draw.rect(screen , white , ground_rect , 5)

    trex = pygame.draw.rect(screen , green , trex_rect)


    score_text = font.render(f"Score: {score}" , True , white)
    score_rect = score_text.get_rect(midtop = (50 , 0))
    screen.blit(score_text,score_rect)

    best_text = font.render(f"Best score: {best_score}" , True , white)
    best_rect = best_text.get_rect(midtop = (200 , 0))
    screen.blit(best_text,best_rect)

    clock.tick(fps)
    pygame.display.update()
pygame.quit()