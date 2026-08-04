import pygame
import random
import os

file_path = os.path.dirname(os.path.abspath(__file__))

pygame.init()
pygame.mixer.init()

# Screen
width = 1200
height = 800
game_state = "PLAY"

# Frame Per Second
fps = 60
clock = pygame.time.Clock()

# Color
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)
trex_color = green

dark_green = (0,180,0)

# Font
font = pygame.font.SysFont(None,30)
over_font = pygame.font.SysFont(None,70)

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
trex_y =  ground_y - trex_height

trex_rect = pygame.Rect(trex_x,trex_y,trex_width,trex_height)

is_grounded = True

# Physics
gravity = 1
vy_trex = 0

# Animation
animation_timer = 0
animation_index = 0

# Cactus
cactus = {
    "cactus_x": width,
    "cactus_y": ground_y - 60,
    "cactus_width": 30,
    "cactus_height": 60,
    "cactus_speed": 8,
    "cactus_color":red
}

cactus_rect = (cactus["cactus_x"],
               cactus["cactus_y"],
               cactus["cactus_width"],
               cactus["cactus_height"]
)

# Clouds
clouds = []

for i in range(3):
    cloud = {"cloud_x": width + random.randint(100,500) +- 120,
            "cloud_y": random.randint(0,height // 2),
            "cloud_width": 80,
            "cloud_height": 40,
            "cloud_color": white,
            "cloud_speed": random.randint(2,3)
    }
    clouds.append(cloud)

# Sounds
jump_path = os.path.join(file_path,"assets","sounds","Mario_Jump.mp3")
jump = pygame.mixer.Sound(jump_path)

Bing_path = os.path.join(file_path,"assets","sounds","Bing_HI.mp3")
Bing = pygame.mixer.Sound(Bing_path)

dead_path = os.path.join(file_path,"assets","sounds","UGH.mp3")
dead = pygame.mixer.Sound(dead_path)

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("T-Rex Game")

running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "PLAY":
                    if is_grounded == True:
                        is_grounded = False
                        vy_trex = -20
                        jump.play()

                elif game_state == "DEAD":
                    screen.fill(black)
                    vy_trex = 0
                    trex_y = ground_y - trex_height
                    is_grounded = True
                    cactus["cactus_x"] = width
                    cactus["cactus_speed"] = 8
                    cloud["cloud_x"] = width
                    score = 0
                    game_state = "PLAY"

    if game_state == "PLAY":
        screen.fill(black)

        frame_count += 1
        if frame_count >= fps // 12:
            score += 1
            if score % 100 == 0:
                Bing.play()
            frame_count = 0

        if is_grounded == False:
            vy_trex += gravity
            trex_y += vy_trex
        elif is_grounded == True:
            vy_trex = 0
            trex_y = ground_y - trex_height
        if trex_y >= ground_y - trex_height:
                is_grounded = True

        if is_grounded == True:
            animation_timer += 1
            if animation_timer >= 8:
                animation_index = (animation_index + 1) % 2
                animation_timer = 0
            if animation_index == 0:
                trex_color = green
            else:
                trex_color = blue
        else:
            trex_color = red

        cactus["cactus_x"] -= cactus["cactus_speed"]
        cactus_rect = (cactus["cactus_x"],
                cactus["cactus_y"],
                cactus["cactus_width"],
                cactus["cactus_height"]
        )
        if cactus["cactus_x"] <= 0 - cactus["cactus_width"]:
            cactus["cactus_x"] = width + random.randint(0,200)

        if trex_rect.colliderect(cactus_rect):
            if score > best_score:
                best_score = score
            dead.play()
            game_state = "DEAD"

        for cloud in clouds:
            cloud["cloud_x"] -= cloud["cloud_speed"]
            cloud_rect = pygame.Rect(cloud["cloud_x"],
                                    cloud["cloud_y"],
                                    cloud["cloud_width"],
                                    cloud["cloud_height"]
            )
            if cloud["cloud_x"] <= 0 - cloud["cloud_width"]:
                cloud["cloud_x"] = width + random.randint(0,200)
                cloud["cloud_y"] = random.randint(0,height // 2)
                cloud["cloud_speed"] = random.randint(2,3)
                cloud["cloud_width"] = random.randint(70,120)
                cloud["cloud_height"] = random.randint(30,50)
            pygame.draw.ellipse(screen, cloud["cloud_color"],cloud_rect) # CLOUD

        if score >= 400:
            cactus["cactus_speed"] = 9
        elif score >= 500:
            cactus["cactus_speed"] = 10
        elif score >= 600:
            cactus["cactus_speed"] = 11
        elif score >= 700:
            cactus["cactus_speed"] = 12
        elif score >= 800:
            cactus["cactus_speed"] = 13
        elif score >= 900:
            cactus["cactus_speed"] = 14
        elif score >= 1000:
            cactus["cactus_speed"] = 15 # MAX SPEED


        trex_rect = pygame.Rect(trex_x,trex_y,trex_width,trex_height)

        ground = pygame.draw.rect(screen , white , ground_rect , 5)

        trex = pygame.draw.rect(screen , trex_color , trex_rect)

        pygame.draw.rect(screen,cactus["cactus_color"], cactus_rect) #CACTUS

        score_text = font.render(f"Score: {score}" , True , white)
        score_rect = score_text.get_rect(midtop = (50 , 0))
        screen.blit(score_text,score_rect)

        best_text = font.render(f"Best score: {best_score}" , True , white)
        best_rect = best_text.get_rect(midtop = (200 , 0))
        screen.blit(best_text,best_rect)

    elif game_state == "DEAD":

        dead_text = over_font.render("GAME OVER" , True , red)
        dead_rect = dead_text.get_rect(center = (width / 2 , height / 2))
        screen.blit(dead_text,dead_rect)

        restart = font.render("Press SPACE to restart" , True , white)
        restart_rect = restart.get_rect(center = (width / 2 , height / 2 + 50))
        screen.blit(restart,restart_rect)

    clock.tick(fps)
    pygame.display.update()
pygame.quit()