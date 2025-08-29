#################################################################################################
# Colony Defender Arcade Game
# 
# August 2025
#################################################################################################

import pygame, sys, time, random, math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 700))
pygame.display.set_caption('COLONY DEFENDER')

# Create spacecraft icon
def create_spacecraft_icon():
    # Create a 32x32 surface for the icon
    icon_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
    icon_surface.fill((0, 0, 0, 0))  # Transparent background
    
    # Create Mac-style rounded rectangle background with proper rounded edges
    corner_radius = 7
    grey_color = (80, 80, 80)  # Medium grey background
    
    # Create a mask for rounded rectangle with smooth anti-aliased edges
    for x in range(32):
        for y in range(32):
            # Calculate distance from corners with anti-aliasing
            alpha = 255  # Full opacity by default
            
            if x < corner_radius and y < corner_radius:
                # Top-left corner
                dist = ((x - corner_radius + 0.5) ** 2 + (y - corner_radius + 0.5) ** 2) ** 0.5
                if dist > corner_radius:
                    continue  # Outside corner, leave transparent
                elif dist > corner_radius - 1:
                    # Anti-aliasing zone
                    alpha = int(255 * (corner_radius - dist))
            elif x >= 32 - corner_radius and y < corner_radius:
                # Top-right corner
                dist = ((x - (32 - corner_radius - 0.5)) ** 2 + (y - corner_radius + 0.5) ** 2) ** 0.5
                if dist > corner_radius:
                    continue
                elif dist > corner_radius - 1:
                    alpha = int(255 * (corner_radius - dist))
            elif x < corner_radius and y >= 32 - corner_radius:
                # Bottom-left corner
                dist = ((x - corner_radius + 0.5) ** 2 + (y - (32 - corner_radius - 0.5)) ** 2) ** 0.5
                if dist > corner_radius:
                    continue
                elif dist > corner_radius - 1:
                    alpha = int(255 * (corner_radius - dist))
            elif x >= 32 - corner_radius and y >= 32 - corner_radius:
                # Bottom-right corner
                dist = ((x - (32 - corner_radius - 0.5)) ** 2 + (y - (32 - corner_radius - 0.5)) ** 2) ** 0.5
                if dist > corner_radius:
                    continue
                elif dist > corner_radius - 1:
                    alpha = int(255 * (corner_radius - dist))
            
            # Set pixel with appropriate alpha for smooth edges
            smooth_color = (grey_color[0], grey_color[1], grey_color[2], alpha)
            icon_surface.set_at((x, y), smooth_color)
    
    # Draw simplified spacecraft (scaled down version)
    center_x, center_y = 16, 16
    
    # Draw black borders for spacecraft elements
    
    # Main body border - black
    pygame.draw.rect(icon_surface, (0, 0, 0), (center_x - 5, center_y + 1, 10, 11), 2)
    
    # Left wing border - black
    pygame.draw.polygon(icon_surface, (0, 0, 0), [
        (center_x - 9, center_y + 7),
        (center_x - 1, center_y + 5),
        (center_x - 1, center_y + 13),
        (center_x - 9, center_y + 15)
    ], 2)
    
    # Right wing border - black
    pygame.draw.polygon(icon_surface, (0, 0, 0), [
        (center_x + 9, center_y + 7),
        (center_x + 1, center_y + 5),
        (center_x + 1, center_y + 13),
        (center_x + 9, center_y + 15)
    ], 2)
    
    # Nose cone border - black
    pygame.draw.polygon(icon_surface, (0, 0, 0), [
        (center_x, center_y - 3),
        (center_x - 4, center_y + 5),
        (center_x + 4, center_y + 5)
    ], 2)
    
    # Now draw the filled colored elements
    
    # Main body (cabin) - silver/gray
    pygame.draw.rect(icon_surface, (192, 192, 192), (center_x - 4, center_y + 2, 8, 9))
    
    # Cockpit window - cyan
    pygame.draw.rect(icon_surface, (0, 255, 255), (center_x - 3, center_y + 3, 6, 4))
    
    # Left wing - orange
    pygame.draw.polygon(icon_surface, (255, 165, 0), [
        (center_x - 8, center_y + 8),
        (center_x - 2, center_y + 6),
        (center_x - 2, center_y + 12),
        (center_x - 8, center_y + 14)
    ])
    
    # Right wing - orange
    pygame.draw.polygon(icon_surface, (255, 165, 0), [
        (center_x + 8, center_y + 8),
        (center_x + 2, center_y + 6),
        (center_x + 2, center_y + 12),
        (center_x + 8, center_y + 14)
    ])
    
    # Nose cone - white
    pygame.draw.polygon(icon_surface, (255, 255, 255), [
        (center_x, center_y - 2),
        (center_x - 3, center_y + 4),
        (center_x + 3, center_y + 4)
    ])
    
    # Engine thrusters - purple with black borders
    pygame.draw.rect(icon_surface, (0, 0, 0), (center_x - 6, center_y + 10, 4, 4), 1)  # Left thruster border
    pygame.draw.rect(icon_surface, (0, 0, 0), (center_x + 2, center_y + 10, 4, 4), 1)  # Right thruster border
    pygame.draw.rect(icon_surface, (128, 0, 128), (center_x - 5, center_y + 11, 2, 2))  # Left thruster
    pygame.draw.rect(icon_surface, (128, 0, 128), (center_x + 3, center_y + 11, 2, 2))  # Right thruster
    
    return icon_surface

# Set the window icon
spacecraft_icon = create_spacecraft_icon()
pygame.display.set_icon(spacecraft_icon)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
SILVER = (192, 192, 192)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Enemy colors
ENEMY_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
    (0, 255, 255), (255, 128, 0), (128, 255, 0), (0, 128, 255), (255, 0, 128)
]

screen.fill(BLACK)

def print_score_life(score, life, hiscore):
    # Clear top area
    pygame.draw.rect(screen, BLACK, (0, 0, 500, 35))
    
    font = pygame.font.SysFont("monospace", 18, bold=True)
    scoretext = font.render("SCORE: " + str(score), 1, WHITE)
    screen.blit(scoretext, (10, 6))
    hiscoretext = font.render("HI SCORE: " + str(hiscore), 1, YELLOW)
    screen.blit(hiscoretext, (160, 6))
    lifetext = font.render("LIVES: " + str(life), 1, WHITE)
    screen.blit(lifetext, (380, 6))

def print_stage_message(stage):
    # Clear center area for stage message
    pygame.draw.rect(screen, BLACK, (75, 280, 350, 120))
    
    # Stage message with big font
    font = pygame.font.SysFont("monospace", 50, bold=True)
    stage_msg = font.render("NEXT STAGE", 1, GREEN)  # Green text
    msg_width = stage_msg.get_width()
    screen.blit(stage_msg, ((500 - msg_width) // 2, 300))
    
    # Stage number
    font = pygame.font.SysFont("monospace", 40, bold=True)
    stage_num_msg = font.render("STAGE " + str(stage), 1, YELLOW)  # Yellow text
    msg_width = stage_num_msg.get_width()
    screen.blit(stage_num_msg, ((500 - msg_width) // 2, 360))

def print_pause_message():
    # Clear center area for pause message
    pygame.draw.rect(screen, BLACK, (75, 280, 350, 120))
    
    # Pause message with red border for visibility
    font = pygame.font.SysFont("monospace", 60, bold=True)
    pause_msg = font.render("PAUSED", 1, CYAN)  # Cyan text
    msg_width = pause_msg.get_width()
    screen.blit(pause_msg, ((500 - msg_width) // 2, 300))
    
    # Instructions
    font = pygame.font.SysFont("monospace", 20)
    inst_msg = font.render("Press P to resume", 1, WHITE)  # White text
    msg_width = inst_msg.get_width()
    screen.blit(inst_msg, ((500 - msg_width) // 2, 360))

def print_gameover(score):
    # Clear center area for game over message
    pygame.draw.rect(screen, BLACK, (75, 280, 350, 200))
    
    font = pygame.font.SysFont("monospace", 50, bold=True)
    textgm = font.render("GAME OVER", 1, RED)
    msg_width = textgm.get_width()
    screen.blit(textgm, ((500 - msg_width) // 2, 300))
    
    font = pygame.font.SysFont("monospace", 20)
    textgm = font.render("FINAL SCORE: " + str(score), 1, WHITE)
    msg_width = textgm.get_width()
    screen.blit(textgm, ((500 - msg_width) // 2, 360))
    
    font = pygame.font.SysFont("monospace", 18, bold=True)
    textgm = font.render("Press SPACE to play again", 1, YELLOW)
    msg_width = textgm.get_width()
    screen.blit(textgm, ((500 - msg_width) // 2, 420))
    
    font = pygame.font.SysFont("monospace", 16)
    textgm = font.render("Press ESC to quit", 1, WHITE)
    msg_width = textgm.get_width()
    screen.blit(textgm, ((500 - msg_width) // 2, 450))

# Static landing page elements - generated once
landing_stars = []
landing_buildings = []
landing_initialized = False

def init_landing_page():
    global landing_stars, landing_buildings, landing_initialized
    if not landing_initialized:
        # Generate static stars
        landing_stars = []
        for i in range(70):
            star_x = random.randint(0, 500)
            star_y = random.randint(0, 600)
            star_brightness = random.randint(100, 255)
            star_size = random.randint(1, 2)
            landing_stars.append([star_x, star_y, star_brightness, star_size])
        
        # Generate static city buildings
        landing_buildings = []
        building_x = 0
        while building_x < 500:
            building_width = random.randint(25, 45)
            building_height = random.randint(15, 35)
            building_color = random.choice([(100, 100, 150), (80, 120, 160), (120, 100, 140), (90, 110, 130)])
            landing_buildings.append([building_x, 700 - building_height, building_width, building_height, building_color])
            building_x += building_width
        
        landing_initialized = True

def print_startgame(hiscore=0):
    # Initialize static elements once
    init_landing_page()
    
    # Clear screen and draw background elements
    screen.fill(BLACK)
    
    # Draw static stars
    for star in landing_stars:
        star_color = (star[2], star[2], star[2])
        pygame.draw.circle(screen, star_color, (star[0], star[1]), star[3])
    
    # Draw static city buildings
    for building in landing_buildings:
        # Main building structure
        pygame.draw.rect(screen, building[4], (building[0], building[1], building[2], building[3]))
        
        # Building windows
        window_rows = building[3] // 8
        for row in range(window_rows):
            for col in range(building[2] // 12):
                window_x = building[0] + 3 + col * 12
                window_y = building[1] + 3 + row * 8
                if (window_x + window_y) % 3 == 0:
                    pygame.draw.rect(screen, YELLOW, (window_x, window_y, 4, 4))
    
    # Draw moon - large gray circle in upper right
    moon_x, moon_y = 400, 80
    pygame.draw.circle(screen, (200, 200, 200), (moon_x, moon_y), 25)
    # Moon craters - darker gray spots
    pygame.draw.circle(screen, (150, 150, 150), (moon_x - 8, moon_y - 5), 4)
    pygame.draw.circle(screen, (150, 150, 150), (moon_x + 6, moon_y + 3), 3)
    pygame.draw.circle(screen, (150, 150, 150), (moon_x - 2, moon_y + 8), 2)
    
    # Draw comet - bright streak across upper left
    comet_x, comet_y = 120, 100
    # Comet head - bright white/yellow
    pygame.draw.circle(screen, WHITE, (comet_x, comet_y), 4)
    pygame.draw.circle(screen, YELLOW, (comet_x, comet_y), 2)
    # Comet tail - fading trail
    for i in range(8):
        tail_x = comet_x - (i + 1) * 6
        tail_y = comet_y + (i + 1) * 3
        tail_brightness = max(50, 255 - i * 30)
        tail_color = (tail_brightness, tail_brightness, tail_brightness // 2)
        pygame.draw.circle(screen, tail_color, (tail_x, tail_y), max(1, 3 - i // 3))
    
    # Rainbow colors for each letter
    letter_colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE, SILVER, RED, ORANGE, YELLOW, GREEN]
    
    font = pygame.font.SysFont("monospace", 45, bold=True)
    title = "COLONY DEFENDER"
    
    # Calculate total width to center the title
    total_width = 0
    letter_widths = []
    for letter in title:
        letter_surface = font.render(letter, 1, WHITE)
        letter_width = letter_surface.get_width()
        letter_widths.append(letter_width)
        total_width += letter_width
    
    # Starting x position to center the title
    start_x = (500 - total_width) // 2
    current_x = start_x
    
    # Draw each letter in different color
    for i, letter in enumerate(title):
        color = letter_colors[i % len(letter_colors)]
        letter_surface = font.render(letter, 1, color)
        screen.blit(letter_surface, (current_x, 200))
        current_x += letter_widths[i]
    
    # Date - small and centered below title
    font_small = pygame.font.SysFont("monospace", 12)
    date_text = font_small.render("2025", 1, SILVER)
    date_width = date_text.get_width()
    screen.blit(date_text, ((500 - date_width) // 2, 260))
    
    # Instructions - centered
    font = pygame.font.SysFont("monospace", 15)
    textgm = font.render("Use arrows to move, SPACE to shoot", 1, WHITE)
    msg_width = textgm.get_width()
    screen.blit(textgm, ((500 - msg_width) // 2, 300))
    
    textgm = font.render("Press any key to start", 1, WHITE)
    msg_width = textgm.get_width()
    screen.blit(textgm, ((500 - msg_width) // 2, 330))
    
    # Display high score if it exists
    if hiscore > 0:
        font_hiscore = pygame.font.SysFont("monospace", 16, bold=True)
        hiscore_text = font_hiscore.render("HIGH SCORE: " + str(hiscore), 1, YELLOW)
        msg_width = hiscore_text.get_width()
        screen.blit(hiscore_text, ((500 - msg_width) // 2, 370))
    
    pygame.display.update()

def main_game(hiscore_in):
    # Game variables
    ship_x = 230
    ship_y = 620
    ship_width = 40
    ship_height = 30
    ship_speed = 5
    
    bullets = []
    bullet_speed = 8
    
    enemies = []
    enemy_bombs = []
    enemy_speed = 1
    bomb_speed = 3
    
    score = 0
    lives = 5
    gameover = False
    hiscore = hiscore_in
    
    # Stage system variables
    current_stage = 1
    stage_message_active = False
    stage_message_timer = 0
    stage_message_duration = 120  # 2 seconds at 60 FPS
    
    # Explosion effect variables
    explosion_active = False
    explosion_particles = []
    explosion_timer = 0
    
    # Pause system variables
    paused = False
    
    # Enemy spawn timer
    enemy_spawn_timer = 0
    enemy_spawn_delay = 60  # Spawn enemy every 60 frames (base rate)
    
    # Star background
    stars = []
    for i in range(70):  # More stars for bigger screen
        star_x = random.randint(0, 500)
        star_y = random.randint(0, 600)  # Only in upper area, not over city
        star_brightness = random.randint(100, 255)
        star_size = random.randint(1, 2)
        stars.append([star_x, star_y, star_brightness, star_size])
    
    # Space city buildings
    city_buildings = []
    building_x = 0
    while building_x < 500:
        building_width = random.randint(25, 45)
        building_height = random.randint(15, 35)
        building_color = random.choice([(100, 100, 150), (80, 120, 160), (120, 100, 140), (90, 110, 130)])
        city_buildings.append([building_x, 700 - building_height, building_width, building_height, building_color])
        building_x += building_width
    
    # Create initial enemies
    for i in range(5):
        enemy_x = random.randint(20, 450)
        enemy_y = random.randint(50, 150)
        enemy_color = random.choice(ENEMY_COLORS)
        enemies.append([enemy_x, enemy_y, enemy_color])
    
    #################################################################################################
    # Main game loop
    #################################################################################################
    while True:
        # Event handling
        was_paused = paused  # Remember previous pause state
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    paused = not paused  # Toggle pause
                elif event.key == K_SPACE and not paused:
                    # Shoot bullet (only when not paused)
                    bullets.append([ship_x + ship_width//2, ship_y])
        
        if gameover:
            print_gameover(score)
            pygame.display.update()
            time.sleep(0.1)
            continue
        
        # If paused, show pause message and skip game logic
        if paused:
            print_pause_message()
            pygame.display.update()
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            continue
        
        # Clear pause message area when resuming from pause
        if was_paused and not paused:
            pygame.draw.rect(screen, BLACK, (75, 280, 350, 120))
        
        time.sleep(0.016)  # ~60 FPS
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw star background
        for star in stars:
            star_color = (star[2], star[2], star[2])  # Gray scale based on brightness
            pygame.draw.circle(screen, star_color, (star[0], star[1]), star[3])
        
        # Draw space city at bottom
        for building in city_buildings:
            # Main building structure
            pygame.draw.rect(screen, building[4], (building[0], building[1], building[2], building[3]))
            
            # Building windows - small yellow squares (static, no blinking)
            window_rows = building[3] // 8  # One row of windows per 8 pixels of height
            for row in range(window_rows):
                for col in range(building[2] // 12):  # One window per 12 pixels of width
                    window_x = building[0] + 3 + col * 12
                    window_y = building[1] + 3 + row * 8
                    # Static windows - use building position to determine which are lit
                    if (window_x + window_y) % 3 == 0:  # Deterministic pattern instead of random
                        pygame.draw.rect(screen, YELLOW, (window_x, window_y, 4, 4))
            

        
        # Handle input
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and ship_x > 0:
            ship_x -= ship_speed
        if keys[K_RIGHT] and ship_x < 500 - ship_width:
            ship_x += ship_speed
        
        # Update bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
        
        # Update enemies
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            # Check if enemy touches the city (around y=665, accounting for building heights)
            if enemy[1] + 24 >= 665:  # Enemy height is 24px
                # Create explosion effect for enemy hitting city
                explosion_active = True
                explosion_timer = 0
                explosion_particles = []
                center_x = enemy[0] + 15  # Center of 30px wide enemy
                center_y = enemy[1] + 12  # Center of 24px tall enemy
                # Create explosion particles with enemy and city colors
                explosion_colors = [enemy[2], YELLOW, ORANGE, RED, WHITE, SILVER]
                for i in range(20):  # 20 particles for city impact
                    particle_x = center_x + random.randint(-15, 15)
                    particle_y = center_y + random.randint(-10, 10)
                    vel_x = random.randint(-6, 6)
                    vel_y = random.randint(-6, 6)
                    color = random.choice(explosion_colors)
                    size = random.randint(2, 4)
                    explosion_particles.append([particle_x, particle_y, vel_x, vel_y, color, size])
                
                enemies.remove(enemy)
                lives -= 1  # Lose life when enemy hits city
            # Remove enemies that go completely off screen
            elif enemy[1] > 700:
                enemies.remove(enemy)
        
        # Enemy shooting
        for enemy in enemies:
            if random.randint(1, 200) == 1:  # Random chance to shoot
                enemy_bombs.append([enemy[0] + 10, enemy[1] + 15])
        
        # Update enemy bombs
        for bomb in enemy_bombs[:]:
            bomb[1] += bomb_speed
            if bomb[1] > 700:
                enemy_bombs.remove(bomb)
        
        # Collision: bullets vs enemies (updated for bigger fly enemies)
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (bullet[0] >= enemy[0] and bullet[0] <= enemy[0] + 30 and
                    bullet[1] >= enemy[1] and bullet[1] <= enemy[1] + 24):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    
                    # Update high score if current score is higher
                    if score > hiscore:
                        hiscore = score
                    
                    # Check for stage progression every 200 points
                    new_stage = (score // 200) + 1
                    if new_stage > current_stage:
                        current_stage = new_stage
                        stage_message_active = True
                        stage_message_timer = 0
                        # Increase enemy speed and bomb speed by 10% each stage
                        enemy_speed = enemy_speed * 1.1
                        bomb_speed = bomb_speed * 1.1
                        # Increase enemy spawn rate by 50% (reduce delay by 33%)
                        enemy_spawn_delay = int(enemy_spawn_delay * 0.67)
                    break
        
        # Collision: bombs vs ship
        for bomb in enemy_bombs[:]:
            if (bomb[0] >= ship_x and bomb[0] <= ship_x + ship_width and
                bomb[1] >= ship_y and bomb[1] <= ship_y + ship_height):
                enemy_bombs.remove(bomb)
                lives -= 1
                # Create explosion effect
                explosion_active = True
                explosion_timer = 0
                explosion_particles = []
                center_x = ship_x + ship_width // 2
                center_y = ship_y + ship_height // 2
                # Create explosion particles with ship colors
                explosion_colors = [SILVER, ORANGE, WHITE, CYAN, PURPLE, YELLOW, RED]
                for i in range(25):  # 25 particles
                    particle_x = center_x + random.randint(-20, 20)
                    particle_y = center_y + random.randint(-15, 15)
                    vel_x = random.randint(-8, 8)
                    vel_y = random.randint(-8, 8)
                    color = random.choice(explosion_colors)
                    size = random.randint(2, 5)
                    explosion_particles.append([particle_x, particle_y, vel_x, vel_y, color, size])
        
        # Update stage message timer
        if stage_message_active:
            stage_message_timer += 1
            if stage_message_timer >= stage_message_duration:
                stage_message_active = False
        
        # Update explosion effect
        if explosion_active:
            explosion_timer += 1
            # Update particle positions
            for particle in explosion_particles:
                particle[0] += particle[2]  # x += vel_x
                particle[1] += particle[3]  # y += vel_y
                particle[3] += 0.3  # Add gravity to vel_y
                particle[5] = max(1, particle[5] - 0.1)  # Shrink particle size
            
            # Remove particles that are too small or off screen
            explosion_particles = [p for p in explosion_particles if p[5] > 1 and p[1] < 750]
            
            # End explosion after 60 frames or no particles left
            if explosion_timer > 60 or len(explosion_particles) == 0:
                explosion_active = False
        
        # Spawn new enemies
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_delay:
            enemy_x = random.randint(20, 450)
            enemy_y = random.randint(30, 80)
            enemy_color = random.choice(ENEMY_COLORS)
            enemies.append([enemy_x, enemy_y, enemy_color])
            enemy_spawn_timer = 0
        
        # Draw spaceship - more detailed design
        center_x = ship_x + ship_width // 2
        
        # Main body (cabin) - silver/gray
        pygame.draw.rect(screen, SILVER, (center_x - 8, ship_y + 8, 16, 18))
        
        # Cockpit window - cyan
        pygame.draw.rect(screen, CYAN, (center_x - 6, ship_y + 10, 12, 8))
        
        # Left wing - orange
        pygame.draw.polygon(screen, ORANGE, [
            (ship_x, ship_y + 20),
            (ship_x + 12, ship_y + 15),
            (ship_x + 12, ship_y + 25),
            (ship_x, ship_y + 28)
        ])
        
        # Right wing - orange
        pygame.draw.polygon(screen, ORANGE, [
            (ship_x + ship_width, ship_y + 20),
            (ship_x + ship_width - 12, ship_y + 15),
            (ship_x + ship_width - 12, ship_y + 25),
            (ship_x + ship_width, ship_y + 28)
        ])
        
        # Nose cone - white
        pygame.draw.polygon(screen, WHITE, [
            (center_x, ship_y),
            (center_x - 6, ship_y + 12),
            (center_x + 6, ship_y + 12)
        ])
        
        # Engine thrusters - purple/blue
        pygame.draw.rect(screen, PURPLE, (center_x - 10, ship_y + 26, 4, 4))
        pygame.draw.rect(screen, PURPLE, (center_x + 6, ship_y + 26, 4, 4))
        
        # Wing tips - yellow accents
        pygame.draw.circle(screen, YELLOW, (ship_x + 2, ship_y + 24), 2)
        pygame.draw.circle(screen, YELLOW, (ship_x + ship_width - 2, ship_y + 24), 2)
        
        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(screen, YELLOW, (int(bullet[0]), int(bullet[1])), 3)
        
        # Draw enemies - fly-like shape
        for enemy in enemies:
            center_x = enemy[0] + 15  # Center of 30px wide enemy
            center_y = enemy[1] + 12  # Center of 24px tall enemy
            
            # Body - oval shape
            pygame.draw.ellipse(screen, enemy[2], (enemy[0] + 8, enemy[1] + 8, 14, 8))
            
            # Wings - left and right
            wing_color = (min(255, enemy[2][0] + 50), min(255, enemy[2][1] + 50), min(255, enemy[2][2] + 50))
            # Left wing
            pygame.draw.ellipse(screen, wing_color, (enemy[0], enemy[1] + 4, 12, 16))
            # Right wing  
            pygame.draw.ellipse(screen, wing_color, (enemy[0] + 18, enemy[1] + 4, 12, 16))
            
            # Head - small circle
            head_color = (max(0, enemy[2][0] - 30), max(0, enemy[2][1] - 30), max(0, enemy[2][2] - 30))
            pygame.draw.circle(screen, head_color, (center_x, enemy[1] + 6), 4)
            
            # Eyes - tiny white dots
            pygame.draw.circle(screen, WHITE, (center_x - 2, enemy[1] + 5), 1)
            pygame.draw.circle(screen, WHITE, (center_x + 2, enemy[1] + 5), 1)
        
        # Draw enemy bombs
        for bomb in enemy_bombs:
            pygame.draw.circle(screen, YELLOW, (int(bomb[0]), int(bomb[1])), 4)
        
        # Draw explosion particles
        if explosion_active:
            for particle in explosion_particles:
                pygame.draw.circle(screen, particle[4], (int(particle[0]), int(particle[1])), int(particle[5]))
        
        # Draw stage message if active
        if stage_message_active:
            print_stage_message(current_stage)
        
        # Check game over
        if lives <= 0:
            gameover = True
        
        # Update display
        print_score_life(score, lives, hiscore)
        pygame.display.update()
        
        # Return both score and hiscore when game over
        if gameover:
            return score, hiscore

######################################################################################
# MAIN GAME LOOP
######################################################################################

game_state = "start"  # "start", "playing", "gameover"
final_score = 0
hiscore = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game_state == "start":
                # Start the game
                screen.fill(BLACK)
                game_state = "playing"
                final_score, hiscore = main_game(hiscore)
                game_state = "gameover"
            elif game_state == "gameover":
                if event.key == K_SPACE:
                    # Restart the game
                    screen.fill(BLACK)
                    game_state = "playing"
                    final_score, hiscore = main_game(hiscore)
                    game_state = "gameover"
                elif event.key == K_ESCAPE:
                    # Quit the game
                    pygame.quit()
                    sys.exit()
    
    # Display appropriate screen based on game state
    if game_state == "start":
        print_startgame(hiscore)
    elif game_state == "gameover":
        print_gameover(final_score)
        pygame.display.update()
    
    time.sleep(0.016)  # Small delay to prevent excessive CPU usage