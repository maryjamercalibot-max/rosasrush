import pygame
import random
import math

pygame.init()

# ==========================================
# WINDOW
# ==========================================

WIDTH = 900
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rosas Rush")
clock = pygame.time.Clock()

# ==========================================
# COLORS
# ==========================================

BACKGROUND = (18, 10, 45)
WHITE = (255, 255, 255)
PINK = (255, 125, 180)
ROSE_RED = (220, 65, 110)
PURPLE = (100, 75, 150)
YELLOW = (255, 225, 120)
GREEN = (100, 190, 130)
NEON_PURPLE = (150, 60, 255)
CYAN = (80, 230, 255)
DARK_PURPLE = (45, 25, 85)

# ==========================================
# FONTS
# ==========================================

title_font = pygame.font.Font(None, 64)
small_font = pygame.font.Font(None, 28)

# ==========================================
# BACKGROUND SETTINGS
# ==========================================

sky_stars = [
    (
        random.randint(0, WIDTH),
        random.randint(15, 300),
        random.randint(1, 3)
    )
    for _ in range(80)
]

mountain_offset = 0
tree_offset = 0
cloud_offset = 0

mountain_speed = 0.5
tree_speed = 1.5
cloud_speed = 0.3

ground_texture_offset = 0

# Mushroom decorations
next_mushroom_x = 0
mushrooms = []

# Environment decorations
grass_blades = []
fireflies = []
floating_particles = []

# ==========================================
# LEVEL SETTINGS
# ==========================================

GROUND_Y = 430

PLAYER_X = 140
PLAYER_WIDTH = 35
PLAYER_HEIGHT = 40

GRAVITY = 0.7
JUMP_STRENGTH = -15

# ==========================================
# PLAYER
# ==========================================

player = pygame.Rect(
    PLAYER_X,
    GROUND_Y - PLAYER_HEIGHT,
    PLAYER_WIDTH,
    PLAYER_HEIGHT
)

player_y = float(player.y)
player_velocity = 0
on_ground = True

# ==========================================
# LEVEL OBJECTS
# ==========================================

platforms = []
gaps = []
obstacles = []
roses = []
gems = []

# ==========================================
# GAME SETTINGS
# ==========================================

game_speed = 5
score = 0
gem_count = 0
high_score = 0
game_over = False
running = True

next_platform_x = 0
next_gap_x = 0
next_obstacle_x = 0
next_gem_x = 0
next_rose_x = 0

GAP_SAFE_DISTANCE = 300
OBSTACLE_SAFE_DISTANCE = 250


# ==========================================
# DRAW BACKGROUND
# ==========================================

def draw_background():

    global mountain_offset, tree_offset, cloud_offset

    screen.fill(BACKGROUND)

    # Stars
    for x, y, size in sky_stars:
        pygame.draw.circle(screen, WHITE, (x, y), size)

    # Glowing horizon
    pygame.draw.rect(
        screen,
        (35, 15, 75),
        (0, 350, WIDTH, 80)
    )

    pygame.draw.line(
        screen,
        (100, 45, 150),
        (0, 350),
        (WIDTH, 350),
        2
    )

    # Moon
    pygame.draw.circle(screen, YELLOW, (750, 85), 38)
    pygame.draw.circle(screen, BACKGROUND, (770, 70), 34)

    # Clouds
    cloud_offset = (cloud_offset + cloud_speed) % 1100

    for x in range(-200, WIDTH + 200, 350):

        pos = x - cloud_offset

        pygame.draw.circle(
            screen, (75, 55, 115),
            (int(pos), 115), 18
        )

        pygame.draw.circle(
            screen, (75, 55, 115),
            (int(pos + 22), 105), 23
        )

        pygame.draw.circle(
            screen, (75, 55, 115),
            (int(pos + 48), 115), 18
        )

    # Distant mountains
    mountain_offset = (mountain_offset + mountain_speed) % 300

    for x in range(-300, WIDTH + 300, 300):

        pos = x - mountain_offset

        pygame.draw.polygon(
            screen,
            (48, 30, 100),
            [
                (int(pos), 405),
                (int(pos + 150), 170),
                (int(pos + 300), 405)
            ]
        )

        pygame.draw.line(
            screen,
            (105, 65, 155),
            (int(pos + 150), 170),
            (int(pos + 210), 285),
            3
        )

    # Smaller mountains in front
    for x in range(-400, WIDTH + 400, 400):

        pos = x - mountain_offset * 1.3

        pygame.draw.polygon(
            screen,
            (75, 35, 120),
            [
                (int(pos), 420),
                (int(pos + 200), 270),
                (int(pos + 400), 420)
            ]
        )

    # Foreground trees
    tree_offset = (tree_offset + tree_speed) % 180

    for x in range(-180, WIDTH + 180, 180):

        pos = x - tree_offset

        pygame.draw.rect(
            screen,
            (40, 20, 70),
            (int(pos + 65), 340, 18, 90)
        )

        pygame.draw.polygon(
            screen,
            (75, 30, 110),
            [
                (int(pos + 15), 365),
                (int(pos + 75), 220),
                (int(pos + 135), 365)
            ]
        )

        pygame.draw.polygon(
            screen,
            (105, 40, 140),
            [
                (int(pos + 35), 315),
                (int(pos + 75), 245),
                (int(pos + 115), 315)
            ]
        )


# ==========================================
# DRAW GROUND TEXTURES
# ==========================================

def draw_ground_texture(x, width):

    spacing = 48

    first_x = x - int(
        (x + ground_texture_offset) % spacing
    )

    for pos in range(first_x, x + width + spacing, spacing):

        if pos < x or pos + 30 > x + width:
            continue

        pygame.draw.line(
            screen,
            (130, 75, 190),
            (pos + 8, GROUND_Y + 17),
            (pos + 17, GROUND_Y + 13),
            2
        )

        pygame.draw.line(
            screen,
            CYAN,
            (pos + 20, GROUND_Y + 28),
            (pos + 27, GROUND_Y + 25),
            2
        )

        pygame.draw.circle(
            screen,
            (65, 45, 115),
            (pos + 12, GROUND_Y + 48),
            3
        )

        pygame.draw.circle(
            screen,
            PINK,
            (pos + 34, GROUND_Y + 53),
            2
        )

        pygame.draw.line(
            screen,
            (115, 65, 175),
            (pos + 5, GROUND_Y + 62),
            (pos + 25, GROUND_Y + 62),
            2
        )


# ==========================================
# DRAW MUSHROOMS
# ==========================================

def draw_mushrooms():

    for x, y, size in mushrooms:

        # Mushroom stem
        stem = pygame.Rect(
            x - 4,
            y + 9,
            8,
            size + 8
        )

        pygame.draw.rect(
            screen,
            (190, 155, 205),
            stem,
            border_radius=3
        )

        # Stem shading
        pygame.draw.line(
            screen,
            (125, 95, 155),
            (x + 2, y + 13),
            (x + 2, y + size + 14),
            2
        )

        # Underside of mushroom cap
        pygame.draw.ellipse(
            screen,
            (115, 55, 155),
            (x - size, y + 5, size * 2, 12)
        )

        # Main mushroom cap
        pygame.draw.ellipse(
            screen,
            (155, 65, 190),
            (x - size, y - 5, size * 2, 17)
        )

        # Highlight on cap
        pygame.draw.arc(
            screen,
            (220, 130, 240),
            (x - size + 3, y - 4, size * 2 - 6, 13),
            0.2,
            2.8,
            2
        )

        # Glowing spots
        pygame.draw.circle(
            screen,
            CYAN,
            (x - 5, y + 1),
            2
        )

        pygame.draw.circle(
            screen,
            PINK,
            (x + 5, y + 2),
            2
        )

        # Gills underneath the cap
        for offset in [-5, 0, 5]:

            pygame.draw.line(
                screen,
                (210, 155, 225),
                (x + offset, y + 10),
                (x + offset // 2, y + 15),
                1
            )


# ==========================================
# CREATE ENVIRONMENT
# ==========================================

def create_environment():

    global grass_blades, fireflies, floating_particles

    grass_blades = []
    fireflies = []
    floating_particles = []

    # Grass blades
    for x in range(0, WIDTH + 100, 8):

        grass_blades.append({
            "x": x + random.randint(-3, 3),
            "height": random.randint(5, 15),
            "color": random.choice([
                (120, 70, 180),
                (160, 80, 190),
                (70, 180, 190),
                (220, 100, 170)
            ])
        })

    # Fireflies
    for _ in range(18):

        fireflies.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(80, GROUND_Y - 35),
            "size": random.randint(2, 4),
            "speed": random.uniform(0.3, 1.0),
            "phase": random.uniform(0, 6.28)
        })

    # Floating particles
    for _ in range(35):

        floating_particles.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(30, GROUND_Y - 20),
            "size": random.randint(1, 3),
            "speed": random.uniform(0.2, 0.8),
            "color": random.choice([
                (150, 100, 220),
                (90, 210, 230),
                (255, 130, 190)
            ])
        })


# ==========================================
# UPDATE ENVIRONMENT
# ==========================================

def update_environment():

    # Move grass with the scrolling ground
    for blade in grass_blades:

        blade["x"] -= game_speed

        if blade["x"] < -5:

            blade["x"] = WIDTH + random.randint(5, 25)
            blade["height"] = random.randint(5, 15)

    # Animate fireflies
    for fly in fireflies:

        fly["x"] -= fly["speed"]
        fly["phase"] += 0.04
        fly["y"] += math.sin(fly["phase"]) * 0.5

        if fly["x"] < -10:

            fly["x"] = WIDTH + random.randint(10, 100)
            fly["y"] = random.randint(80, GROUND_Y - 35)

    # Animate floating particles
    for particle in floating_particles:

        particle["x"] -= particle["speed"]
        particle["y"] -= 0.25

        if particle["x"] < -5 or particle["y"] < 20:

            particle["x"] = WIDTH + random.randint(5, 100)
            particle["y"] = random.randint(50, GROUND_Y - 20)


# ==========================================
# DRAW ENVIRONMENT
# ==========================================

def draw_environment():

    current_time = pygame.time.get_ticks()

    # Grass
    for blade in grass_blades:

        x = int(blade["x"])
        height = blade["height"]
        color = blade["color"]

        # Avoid drawing grass over ground gaps
        over_gap = any(
            gap.left <= x <= gap.right
            for gap in gaps
        )

        if not over_gap:

            sway = math.sin(current_time * 0.003 + x) * 2

            pygame.draw.line(
                screen,
                color,
                (x, GROUND_Y),
                (int(x + sway), GROUND_Y - height),
                2
            )

    # Fireflies
    for fly in fireflies:

        x = int(fly["x"])
        y = int(fly["y"])
        size = fly["size"]

        glow = (
            math.sin(current_time * 0.004 + fly["phase"]) + 1
        ) / 2

        brightness = int(130 + glow * 125)

        # Outer glow
        pygame.draw.circle(
            screen,
            (100, 90, 130),
            (x, y),
            size + 4
        )

        # Firefly center
        pygame.draw.circle(
            screen,
            (brightness, brightness, 100),
            (x, y),
            size
        )

    # Floating particles
    for particle in floating_particles:

        pygame.draw.circle(
            screen,
            particle["color"],
            (int(particle["x"]), int(particle["y"])),
            particle["size"]
        )


# ==========================================
# SPAWN PLATFORMS
# ==========================================

def spawn_platform(x):

    width = random.randint(180, 230)
    height = random.choice([300, 320, 340, 355])

    platforms.append(
        pygame.Rect(x, height, width, 18)
    )

    for i in range(3):
        pygame.Rect(
            x + 45 + i * 45,
            height - 55,
            20,
            20
        )


# ==========================================
# SPAWN GROUND GAPS
# ==========================================

def spawn_gap(x):

    width = random.randint(100, 140)

    new_gap = pygame.Rect(
        x,
        GROUND_Y,
        width,
        HEIGHT - GROUND_Y
    )

    gaps.append(new_gap)

    obstacles[:] = [
        obstacle for obstacle in obstacles
        if not (
            obstacle["rect"].right > new_gap.left - GAP_SAFE_DISTANCE
            and obstacle["rect"].left < new_gap.right + GAP_SAFE_DISTANCE
        )
    ]


# ==========================================
# SPAWN OBSTACLES
# ==========================================

def spawn_obstacle(x):

    for gap in gaps:

        if(
            x < gap.right + GAP_SAFE_DISTANCE
            and x + 40 > gap.left - GAP_SAFE_DISTANCE
        ):
            return
    for obstacle in obstacles:

        existing = obstacle["rect"]

        if abs(existing.x - x) < OBSTACLE_SAFE_DISTANCE:
            return

    obstacle_type = random.choice(["spike", "block"])

    if obstacle_type == "spike":

        rect = pygame.Rect(
            x,
            GROUND_Y - 35,
            35,
            35
        )

    else:

        rect = pygame.Rect(
            x,
            GROUND_Y - 50,
            40,
            50
        )

    obstacles.append({
        "rect": rect,
        "type": obstacle_type
    })


# ==========================================
# RESET GAME
# ==========================================

def reset_game():

    global player, player_y, player_velocity
    global on_ground, game_speed, score, game_over
    global next_platform_x, next_gap_x, next_obstacle_x
    global next_mushroom_x, next_gem_x, next_rose_x

    player = pygame.Rect(
        PLAYER_X,
        GROUND_Y - PLAYER_HEIGHT,
        PLAYER_WIDTH,
        PLAYER_HEIGHT
    )

    player_y = float(player.y)
    player_velocity = 0
    on_ground = True

    platforms.clear()
    gaps.clear()
    obstacles.clear()
    roses.clear()
    mushrooms.clear()
    gems.clear()

    spawn_platform(650)

    # Initial mushroom decorations
    for x in range(300, 1800, 250):

        size = random.randint(12, 18)

        mushrooms.append((
            x,
            GROUND_Y - size - 17,
            size
        ))

    gaps.append(
        pygame.Rect(
            1550,
            GROUND_Y,
            130,
            HEIGHT - GROUND_Y
        )
    )

    obstacles.append({
        "rect": pygame.Rect(
            430,
            GROUND_Y - 35,
            35,
            35
        ),
        "type": "spike"
    })

    game_speed = 5
    score = 0
    game_over = False

    next_platform_x = WIDTH + 1400
    next_gap_x = WIDTH + 2200
    next_obstacle_x = WIDTH + 550
    next_mushroom_x = WIDTH + 300
    next_gem_x = WIDTH + 650
    gem_count = 0
    next_rose_x = WIDTH + 350

    # Initialize grass, fireflies, and particles
    create_environment()


reset_game()


# ==========================================
# MAIN GAME LOOP
# ==========================================

while running:

    clock.tick(60)

    # ======================================
    # EVENTS
    # ======================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if game_over:
                    reset_game()

                elif on_ground:
                    player_velocity = JUMP_STRENGTH
                    on_ground = False

    # ======================================
    # UPDATE GAME
    # ======================================

    if not game_over:

        ground_texture_offset += game_speed

        # Move level objects
        for platform in platforms:
            platform.x -= game_speed

        for gap in gaps:
            gap.x -= game_speed

        for obstacle in obstacles:
            obstacle["rect"].x -= game_speed

        for rose in roses:
            rose.x -= game_speed

        for gem in gems:
            gem.x -= game_speed

        # Move mushrooms
        for i in range(len(mushrooms)):

            x, y, size = mushrooms[i]
            mushrooms[i] = (x - game_speed, y, size)

        # Update grass, fireflies, and floating particles
        update_environment()

        # Remove off-screen objects
        platforms[:] = [p for p in platforms if p.right > 0]
        gaps[:] = [g for g in gaps if g.right > 0]

        obstacles[:] = [
            o for o in obstacles
            if o["rect"].right > 0
        ]

        roses[:] = [r for r in roses if r.right > 0]

        gems[:] = [gem for gem in gems if gem.right > 0]

        mushrooms[:] = [
            mushroom for mushroom in mushrooms
            if mushroom[0] > -30
        ]

        # Generate platforms
        next_platform_x -= game_speed

        if next_platform_x < WIDTH:

            spawn_platform(WIDTH)

            next_platform_x = WIDTH + random.randint(1100, 1450)

        # Generate gaps
        next_gap_x -= game_speed

        if next_gap_x < WIDTH:

            spawn_gap(WIDTH)

            next_gap_x = WIDTH + random.randint(1800, 2400)

        # Generate obstacles
        next_obstacle_x -= game_speed

        if next_obstacle_x < WIDTH:

            spawn_obstacle(WIDTH)

            next_obstacle_x = WIDTH + random.randint(550, 750)

        next_gem_x -= game_speed

        if next_gem_x < WIDTH:

            near_gap = any(
                gap.left - 80 <= WIDTH <= gap.right + 80
                for gap in gaps
            )

            near_obstacle = any(
                abs(obstacle["rect"].centerx - WIDTH) < 150
                for obstacle in obstacles
            )

            if not near_gap and not near_obstacle:

                gem_y = random.randint(300, 365)

                gems.append(
                    pygame.Rect(WIDTH, gem_y, 22, 22)
                )

            next_gem_x = WIDTH + random.randint(700, 1000)

        next_rose_x -= game_speed

        if next_rose_x < WIDTH:

            near_gap = any(
                gap.left - 50 <= WIDTH <=gap.right + 50
                for gap in gaps
            )

            if not near_gap:

                rose_y = random.randint(300, 365)

                roses.append(
                    pygame.Rect(WIDTH, rose_y, 18, 18)
                )
            next_rose_x = WIDTH + random.randint(450, 700)


        # Generate mushrooms throughout the level
        next_mushroom_x -= game_speed

        if next_mushroom_x < WIDTH:

            size = random.randint(12, 18)

            # Avoid placing mushrooms near gaps
            near_gap = any(
                gap.left - 30 <= WIDTH <= gap.right + 30
                for gap in gaps
            )

            if not near_gap:

                mushrooms.append((
                    WIDTH,
                    GROUND_Y - size - 17,
                    size
                ))

            next_mushroom_x = WIDTH + random.randint(250, 500)

        # Player physics
        previous_bottom = player.bottom

        player_velocity += GRAVITY
        player_y += player_velocity
        player.y = int(player_y)

        on_ground = False

        # Land on elevated platforms
        if player_velocity >= 0:

            for platform in platforms:

                horizontal_overlap = (
                    player.right > platform.left
                    and player.left < platform.right
                )

                crossed_platform_top = (
                    previous_bottom <= platform.top
                    and player.bottom >= platform.top
                )

                if horizontal_overlap and crossed_platform_top:

                    player.bottom = platform.top
                    player_y = float(player.y)
                    player_velocity = 0
                    on_ground = True
                    break

        # Check gaps
        over_gap = any(
            gap.left <= player.centerx <= gap.right
            for gap in gaps
        )

        # Land on normal ground
        if (
            not on_ground
            and not over_gap
            and player_velocity >= 0
            and player.bottom >= GROUND_Y
            and player.top < GROUND_Y
        ):

            player.bottom = GROUND_Y
            player_y = float(player.y)
            player_velocity = 0
            on_ground = True

        # Fall detection
        if player.top > HEIGHT:
            game_over = True

        # Obstacle collisions
        for obstacle in obstacles:

            rect = obstacle["rect"]

            if obstacle["type"] == "spike":

                collision_rect = pygame.Rect(
                    rect.x + 7,
                    rect.y + 12,
                    rect.width - 14,
                    rect.height - 12
                )

            else:
                collision_rect = rect

            if player.colliderect(collision_rect):
                game_over = True

        # Collect roses
        for rose in roses[:]:

            if player.colliderect(rose):

                roses.remove(rose)
                score += 10

        for gem in gems[:]:

            if player.colliderect(gem):

                gems.remove(gem)
                gem_count += 1
                score += 25

        # Score and speed
        score += 1
        high_score = max(high_score, score)

        game_speed = min(
            10,
            5 + score // 1000
        )

    # ======================================
    # DRAW BACKGROUND
    # ======================================

    draw_background()

    # ======================================
    # DRAW NORMAL GROUND
    # ======================================

    ground_segments = []
    start_x = 0

    for gap in sorted(gaps, key=lambda g: g.left):

        if gap.left > start_x:

            ground_segments.append(
                (start_x, gap.left - start_x)
            )

        start_x = max(start_x, gap.right)

    if start_x < WIDTH:

        ground_segments.append(
            (start_x, WIDTH - start_x)
        )

    for x, width in ground_segments:

        if width > 0:

            pygame.draw.rect(
                screen,
                PURPLE,
                (x, GROUND_Y, width, HEIGHT - GROUND_Y)
            )

            pygame.draw.line(
                screen,
                PINK,
                (x, GROUND_Y),
                (x + width, GROUND_Y),
                4
            )

            draw_ground_texture(x, width)

    # ======================================
    # DRAW GROUND GAP EDGES
    # ======================================

    for gap in gaps:

        pygame.draw.line(
            screen,
            CYAN,
            (gap.left, GROUND_Y),
            (gap.left, HEIGHT),
            3
        )

        pygame.draw.line(
            screen,
            CYAN,
            (gap.right, GROUND_Y),
            (gap.right, HEIGHT),
            3
        )

    # ======================================
    # DRAW GRASS, FIREFLIES, AND PARTICLES
    # ======================================

    draw_environment()

    # ======================================
    # DRAW ELEVATED PLATFORMS
    # ======================================

    for platform in platforms:

        pygame.draw.rect(
            screen,
            DARK_PURPLE,
            platform,
            border_radius=5
        )

        pygame.draw.rect(
            screen,
            NEON_PURPLE,
            platform,
            width=3,
            border_radius=5
        )

        pygame.draw.line(
            screen,
            CYAN,
            (platform.left + 8, platform.top + 3),
            (platform.right - 8, platform.top + 3),
            3
        )

        pygame.draw.line(
            screen,
            PURPLE,
            (platform.left + 25, platform.bottom),
            (platform.left + 25, platform.bottom + 25),
            3
        )

        pygame.draw.line(
            screen,
            PURPLE,
            (platform.right - 25, platform.bottom),
            (platform.right - 25, platform.bottom + 25),
            3
        )

    # ======================================
    # DRAW OBSTACLES
    # ======================================

    for obstacle in obstacles:

        rect = obstacle["rect"]

        if obstacle["type"] == "spike":

            pygame.draw.polygon(
                screen,
                (35, 10, 25),
                [
                    (rect.left - 3, rect.bottom + 2),
                    (rect.centerx, rect.top - 3),
                    (rect.right + 3, rect.bottom + 2)
                ]
            )

            pygame.draw.polygon(
                screen,
                (255, 65, 55),
                [
                    (rect.left, rect.bottom),
                    (rect.centerx, rect.top),
                    (rect.right, rect.bottom)
                ]
            )

            pygame.draw.polygon(
                screen,
                (255, 190, 75),
                [
                    (rect.left + 8, rect.bottom - 4),
                    (rect.centerx, rect.top + 12),
                    (rect.right - 8, rect.bottom -4)
                ]
            )

            pygame.draw.polygon(
                screen,
                (255, 95, 45),
                [
                    (rect.left + 12, rect.bottom - 5),
                    (rect.centerx, rect.top + 17),
                    (rect.right - 12, rect.bottom - 5)
                ]
            )

        else:

            shadow_rect = rect.move(4, 4)

            pygame.draw.rect(
                screen,
                (35, 10, 30),
                shadow_rect, border_radius=4
            )

            pygame.draw.rect(
                screen,
                (255, 75, 55),
                rect,
                border_radius=4
            )

            pygame.draw.rect(
                screen,
                (255, 105, 75),
                rect,
                width=4,
                border_radius=4
            )

            stripe_spacing = 15

            for x in range(rect.left + 8, rect.right - 5, stripe_spacing):

                pygame.draw.line(
                    screen,
                    (255, 180, 65),
                    (x, rect.top + 7),
                    (x + 9, rect.bottom -7),
                    3
                )

    # ======================================
    # DRAW ROSES
    # ======================================

    for rose in roses:

        pygame.draw.circle(screen, PINK, rose.center, 9)

        pygame.draw.circle(
            screen,
            ROSE_RED,
            (rose.centerx - 4, rose.centery - 3),
            4
        )

        pygame.draw.line(
            screen,
            GREEN,
            (rose.centerx, rose.bottom - 1),
            (rose.centerx + 5, rose.bottom + 5),
            2
        )
    for gem in gems:

        pygame.draw.circle(
            screen,
            (55, 105, 155),
            gem.center,
            17
        )

        pygame.draw.polygon(
            screen,
            CYAN,
            [
                (gem.centerx, gem.top),
                (gem.right, gem.centery),
                (gem.centerx, gem.bottom),
                (gem.left, gem.centery)
            ]
        )

        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (gem.centerx, gem.top + 5),
                (gem.right - 6,gem.centery),
                (gem.centerx, gem.bottom - 5),
                (gem.left + 6, gem.centery)
            ]
        )
    # ======================================
    # DRAW MUSHROOMS
    # ======================================

    draw_mushrooms()

    # ======================================
    # DRAW PLAYER
    # ======================================

    pygame.draw.rect(
        screen,
        YELLOW,
        player,
        border_radius=6
    )

    pygame.draw.circle(
        screen,
        BACKGROUND,
        (player.x + 24, player.y + 12),
        3
    )

    # ======================================
    # TITLE AND SCORE
    # ======================================

    title = title_font.render(
        "ROSAS RUSH",
        True,
        PINK
    )

    screen.blit(title, (25, 20))

    score_text = small_font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(score_text, (25, 80))

    gem_text = small_font.render(
        f"Gems: {gem_count}",
        True,
        CYAN
    )

    best_text = small_font.render(
        f"Best: {high_score}",
        True,
        YELLOW

    )

    screen.blit(gem_text, (25, 110))
    screen.blit(best_text, (25, 140))

    # ======================================
    # GAME OVER
    # ======================================

    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((10, 5, 25))
        screen.blit(overlay, (0, 0))

        message = title_font.render(
            "GAME OVER",
            True,
            PINK
        )

        restart = small_font.render(
            "Press SPACE to try again",
            True,
            WHITE
        )

        screen.blit(
            message,
            message.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 25)
            )
        )

        screen.blit(
            restart,
            restart.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 30)
            )
        )

    pygame.display.flip()

pygame.quit()