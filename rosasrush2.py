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

#==========================================
# GAME STATES
#===========================================

MENU = "menu"
PLAYING = "playing"
HOW_TO_PLAY = "how_to_play"

game_state = MENU


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
NEON_CYAN = (0, 240, 255)
DARK_PURPLE = (45, 25, 85)

# ==========================================
# FONTS
# ==========================================

title_font = pygame.font.Font(None, 64)
small_font = pygame.font.Font(None, 28)
achievement_font = pygame.font.Font(None, 32)

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
cube_angle = 0

player_scale_x = 1.0
player_scale_y = 1.0
target_scale_x = 1.0
target_scale_y = 1.0

animation_speed = 0.2
player_animation_timer = 0

# ==========================================
# LEVEL OBJECTS
# ==========================================

platforms = []
gaps = []
obstacles = []
roses = []
gems = []
saws = []
jump_orbs = []
jump_pads = []
death_particles = []
jump_trail = []
landing_particles = []
combo = 0
combo_timer = 0
COMBO_DURATION = 180
combo_bonus = 0
game_over_alpha = 0
shockwave_radius = 0
shockwave_alpha = 255
death_effect_started = False

achievements = {
    "first_bloom": {
        "name": "First Bloom",
        "description": "Collect your first gem",
        "unlocked": False
    },

    "gem_collector": {
        "name": "Gem Collector",
        "description": "Collect 10 gems",
        "unlocked": False
    },

    "combo_starter": {
        "name": "Combo Starter",
        "description": "Reach a 5x combo",
        "unlocked": False
    },

    "high_scorer":{
        "name": "High Scorer",
        "description": "Reach 1,000 points",
        "unlocked": False
    }
}

achievement_notifications = []
show_achievements = False

def unlock_achievement(achievement_id):

    achievement = achievements[achievement_id]

    if not achievement["unlocked"]:

        achievement["unlocked"] = True

        achievement_notifications.append({
            "name": achievement["name"],
            "description": achievement["description"],
            "timer": 240
        })

        print("ACHIEVEMENT UNLOCKED:", achievement["name"])

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
next_saw_x = 0

GAP_SAFE_DISTANCE = 300
OBSTACLE_SAFE_DISTANCE = 250

def draw_polygon_glow(surface, points, color):

    glow_surface = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    center_x = sum(p[0] for p in points) / len(points)
    center_y = sum(p[1] for p in points) / len(points)

    outer_points = [
        (
            int(center_x + (x - center_x) * 1.5),
            int(center_y + (y - center_y) * 1.5)
        )
        for x, y in points
    ]

    pygame.draw.lines(
        glow_surface,
        (*color, 25),
        True,
        outer_points,
        12
    )

    pygame.draw.lines(
        glow_surface,
        (*color, 55),
        True,
        points,
        6
    )

    surface.blit(glow_surface, (0,0))


def draw_saw(surface, x, y, radius, angle):

    center = (int(x), int(y))
    teeth = 12

# outer glow
    pygame.draw.circle(
        surface,
        (65, 20, 110),
        center,
        radius + 9
    )

# saw teeth
    points = []

    for i in range(teeth * 2):
        current_angle =  math.radians(
            angle + i * (360 / (teeth * 2))
        )

        if i % 2 == 0:
            distance = radius + 8
        else:
            distance = radius - 3

        px = x + math.cos(current_angle) * distance
        py = y + math.sin(current_angle) * distance

        points.append((int(px), int(py)))

    pygame.draw.polygon(
        surface,
        (255, 65, 180),
        points
    )

    pygame.draw.polygon(
        surface,
        (80, 230, 255),
        points,
        2
    )

    #inner body
    pygame.draw.circle(
        surface,
        (65, 25, 115),
        center,
        radius - 7
    )

    pygame.draw.circle(
        surface,
        (180, 65, 255),
        center,
        radius - 7,
        3
    )

    pygame.draw.circle(
        surface,
        (80, 230, 255),
        center,
        6
    )

# particle
def create_death_effect():

    global death_particles
    global shockwave_radius, shockwave_alpha

    shockwave_radius = 5
    shockwave_alpha = 255

    death_particles = []

    colors = [
        PINK,
        ROSE_RED,
        NEON_PURPLE,
        CYAN,
        WHITE
    ]

    for _ in range(35):

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(3, 10)

        death_particles.append({
            "x": player.centerx,
            "y": player.centery,
            "vx": math.cos(angle) * speed,
            "vy": math.sin(angle) * speed,
            "size": random.randint(4, 8),
            "color": random.choice(colors),
            "life": 45,
            "max_life": 45
        })

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

    for saw in saws:

        if (
            x < saw["x"] + saw["radius"] + GAP_SAFE_DISTANCE
            and x + width > saw["x"] - saw["radius"] - GAP_SAFE_DISTANCE
        ):
            return

    for obstacle in obstacles:

        rect = obstacle["rect"]

        if (
            x < rect.right + GAP_SAFE_DISTANCE
            and x + width > rect.left - GAP_SAFE_DISTANCE
        ):
            return

    new_gap = pygame.Rect(
        x,
        GROUND_Y,
        width,
        HEIGHT - GROUND_Y
    )

    gaps.append(new_gap)


# ==========================================
# SPAWN OBSTACLES
# ==========================================

def spawn_obstacle(x):
    
    obstacle_type = random.choices([
      "spike",
      "double_spike",
      "triple_spike",
      "block",
      "moving_block",
      "hanging_spike"
  ],
  weights=[1, 1, 1, 1, 5, 5],
  k=1
  )[0]
    
    if obstacle_type == "double_spike":
      spike_count = 2
      
    elif obstacle_type == "triple_spike":
      spike_count = 3

    else:
        spike_count = 1
        
    if obstacle_type in ["block", "moving_block"]:
        obstacle_width = 45

    elif obstacle_type == "hanging_spike":
        obstacle_width = 35

    else:
        obstacle_width = spike_count * 35

    for gap in gaps:

        if (
            x < gap.right + GAP_SAFE_DISTANCE
            and x + obstacle_width > gap.left - GAP_SAFE_DISTANCE
        ):
            return

    for obstacle in obstacles:

        existing = obstacle["rect"]

        if abs(existing.x - x) < OBSTACLE_SAFE_DISTANCE:
            return

    for saw in saws:
            if(
                x < saw["x"] + saw["radius"] + OBSTACLE_SAFE_DISTANCE
                and x + obstacle_width > saw["x"] - saw["radius"] - OBSTACLE_SAFE_DISTANCE
            ):
                return

    if obstacle_type in ["spike", "double_spike", "triple_spike"]:

        for i in range(spike_count):

            rect = pygame.Rect(
                x + (i * 35),
                GROUND_Y - 35,
                35,
                35
            )

            obstacles.append({
                "rect": rect,
                "type": "spike"
            })
    elif obstacle_type == "block":
        rect = pygame.Rect(x, GROUND_Y - 50, 40, 50)
        obstacles.append({"rect": rect, "type": "block"})

    elif obstacle_type == "moving_block":
        rect = pygame.Rect(x, GROUND_Y - 100, 45, 45)
        obstacles.append({
            "rect": rect,
            "type": "moving_block",
            "base_y": GROUND_Y - 100,
            "phase": random.uniform(0, 6.28),
            "amplitude": random.randint(35, 65)
        })

    elif obstacle_type == "hanging_spike":
        rect = pygame.Rect(x, 250, 45, 70)

        obstacles.append({
            "rect": rect,
            "type": "hanging_spike"
        })

    


def spawn_saw(x):

    for gap in gaps:

        if(
            x < gap.right + GAP_SAFE_DISTANCE
            and x + 50 > gap.left - GAP_SAFE_DISTANCE
        ):
            return

    for obstacle in obstacles:

        if abs(obstacle["rect"].centerx - x) < OBSTACLE_SAFE_DISTANCE:
            return
    for saw in saws:
        if abs(saw["x"] - x) < 150:
            return
    saws.append({
        "x": x,
        "y": GROUND_Y,
        "radius": 25,
        "angle": 0,
        "grounded": True
    })

#spawn jump orbs

def spawn_jump_orb(x):

    for gap in gaps:
        if gap.left - 100 < x < gap.right + 100:
            return

    rect = pygame.Rect(x, 285, 30, 30)

    jump_orbs.append({
        "rect": rect,
        "pulse": 0
    })

#spawn jump pads

def spawn_jump_pad(x):

    for gap in gaps:
        if x < gap.right + 100 and x + 50 > gap.left - 100:
            return

    rect = pygame.Rect(x, GROUND_Y - 12, 50, 12)

    jump_pads.append(rect)


# ==========================================
# RESET GAME
# ==========================================

def reset_game():

    global player, player_y, player_velocity
    global on_ground, game_speed, score, gem_count, game_over
    global next_platform_x, next_gap_x, next_obstacle_x
    global next_mushroom_x, next_gem_x, next_rose_x, next_saw_x
    global cube_angle
    global next_orb_x, next_pad_x
    global death_effect_started, death_particles
    global game_over_alpha
    global player_scale_x, player_scale_y
    global target_scale_x, target_scale_y
    global player_animation_timer
    global combo, combo_timer, combo_bonus

    player = pygame.Rect(
        PLAYER_X,
        GROUND_Y - PLAYER_HEIGHT,
        PLAYER_WIDTH,
        PLAYER_HEIGHT
    )

    player_y = float(player.y)
    player_velocity = 0
    on_ground = True
    cube_angle = 0
    death_effect_started = False
    game_over_alpha = 0

    combo = 0
    combo_timer = 0
    combo_bonus = 0

    for achievement in achievements.values():
        achievement["unlocked"] = False

    achievement_notifications.clear()

    player_scale_x = 1.0
    player_scale_y = 1.0

    target_scale_x = 1.0
    target_scale_y = 1.0


    player_animation_timer = 0


    platforms.clear()
    gaps.clear()
    obstacles.clear()
    roses.clear()
    mushrooms.clear()
    gems.clear()
    saws.clear()
    jump_orbs.clear()
    jump_pads.clear()
    death_particles.clear()
    jump_trail.clear()
    landing_particles.clear()

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
    next_saw_x = WIDTH + 1200
    next_orb_x = WIDTH + 1000
    next_pad_x = WIDTH + 1600

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

            if game_state == MENU:

                if event.key == pygame.K_RETURN:
                    game_state = PLAYING

                elif event.key == pygame.K_h:
                    game_state = HOW_TO_PLAY

                elif event.key == pygame.K_ESCAPE:
                    running = False

            elif game_state == HOW_TO_PLAY:

                if event.key == pygame.K_ESCAPE:
                    game_state = MENU


            if event.key == pygame.K_a and not game_over and game_state == PLAYING:
                show_achievements = not show_achievements

            if event.key == pygame.K_SPACE and game_state == PLAYING:

                if game_over:
                    reset_game()


                else:
                    touching_orb = False

                    for orb in jump_orbs:

                        orb_area = orb["rect"].inflate(24, 24)

                        if player.colliderect(orb_area):
                            touching_orb = True
                            break

                    if touching_orb and not on_ground:

                        player_velocity = -19
                        on_ground = False

                    elif on_ground:

                        target_scale_x = 0.85
                        target_scale_y = 1.2

                        player_animation_timer = 8

                        player_velocity = JUMP_STRENGTH
                        on_ground = False


    # ======================================
    # UPDATE GAME
    # ======================================

    if game_state == PLAYING and not game_over and not show_achievements:

        ground_texture_offset += game_speed

        # Move level objects
        for platform in platforms:
            platform.x -= game_speed

        for gap in gaps:
            gap.x -= game_speed

        for obstacle in obstacles:
            obstacle["rect"].x -= game_speed

            if obstacle["type"] == "moving_block":

                obstacle["phase"] += 0.06

                obstacle["rect"].y = int(
                    obstacle["base_y"]
                    + math.sin(obstacle["phase"]) * obstacle["amplitude"]
                )

        for saw in saws:
            saw["x"] -= game_speed
            saw["angle"] += 8


        for rose in roses:
            rose.x -= game_speed

        for gem in gems:
            gem.x -= game_speed

        for orb in jump_orbs:
            orb["rect"].x -= game_speed
            orb["pulse"] += 0.08

        for pad in jump_pads:
            pad.x -= game_speed

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

        saws[:] = [
            saw for saw in saws
            if saw["x"] + saw["radius"] > 0
        ]

        roses[:] = [r for r in roses if r.right > 0]

        gems[:] = [gem for gem in gems if gem.right > 0]

        jump_orbs[:] = [
            orb for orb in jump_orbs
            if orb["rect"].right > 0
        ]

        jump_pads[:] = [
            pad for pad in jump_pads 
            if pad.right > 0
        ]

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

        next_saw_x -= game_speed

        if next_saw_x < WIDTH:

            spawn_saw(WIDTH)

            next_saw_x = WIDTH + random.randint(1200, 1700)

        next_orb_x -= game_speed

        if next_orb_x < WIDTH:

            spawn_jump_orb(WIDTH)

            next_orb_x = WIDTH + random.randint(1000, 1500)

        next_pad_x -= game_speed

        if next_pad_x < WIDTH:

            spawn_jump_pad(WIDTH)

            next_pad_x = WIDTH + random.randint(1200, 1800)

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

        # smooth player animation

        if player_animation_timer > 0:
            player_animation_timer -= 1
        else:
            target_scale_x = 1.0
            target_scale_y = 1.0

        player_scale_x += (
            target_scale_x - player_scale_x
        ) * animation_speed

        player_scale_y += (
            target_scale_y - player_scale_y
        ) * animation_speed


        # Player physics
        previous_bottom = player.bottom

        player_velocity += GRAVITY
        player_y += player_velocity
        player.y = int(player_y)

        if not on_ground:
            cube_angle = (cube_angle + 6) % 360
        else:
            cube_angle = round(cube_angle / 90) * 90

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

                    target_scale_x = 1.2
                    target_scale_y = 0.8
                    player_animation_timer = 8

                    #create landing dust particles
                    for _ in range(8):
                        landing_particles.append({
                            "x": player.centerx + random.randint(-12, 12),
                            "y": player.bottom,
                            "size": random.randint(3, 6),
                            "life": 18,
                            "max_life": 18,
                            "color": random.choice([
                                PINK,
                                NEON_PURPLE,
                                CYAN
                            ])
                        })
                    break


        # jump pad collision

        if player_velocity >= 0:

            for pad in jump_pads:

                horizontal_overlap = (
                    player.right > pad.left
                    and player.left < pad.right
                )

                crossed_pad_top = (
                    previous_bottom <= pad.top
                    and player.bottom >= pad.top
                )

                if horizontal_overlap and crossed_pad_top:
                    player.bottom = pad.top
                    player_y = float(player.y)
                    player_velocity = -19
                    on_ground = False

                    #create jump pad particles
                    for _ in range(12):
                        landing_particles.append({
                            "x": player.centerx + random.randint(-15, 15),
                            "y": pad.top,
                            "size": random.randint(3, 7),
                            "life": 22,
                            "max_life": 22,
                            "color": random.choice([
                                PINK,
                                NEON_PURPLE,
                                CYAN,
                                WHITE
                            ])
                        })
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

            target_scale_x = 1.2
            target_scale_y = 0.8

            player_animation_timer = 8

            # create landing dust particles
            for _ in range(8):
                landing_particles.append({
                    "x": player.centerx + random.randint(-12, 12),
                    "y": player.bottom,
                    "size": random.randint(3, 6),
                    "life": 18,
                    "max_life": 18,
                    "color": random.choice([
                        PINK,
                        NEON_PURPLE,
                        CYAN
                    ])
                })

        #create jump trail particles
        if not on_ground and random.random() < 0.35:

            jump_trail.append({
                "x": player.left,
                "y": player.centery,
                "size": random.randint(3, 6),
                "life": 20,
                "max_life": 20,
                "color": random.choice([
                    NEON_PURPLE,
                    PINK,
                    CYAN
                ])
            })



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

            elif obstacle["type"] == "hanging_spike":

                collision_rect = pygame.Rect(
                    rect.x + 7,
                    rect.y,
                    rect.width - 14,
                    rect.height - 12
                )

            else:
                collision_rect = rect

            if player.colliderect(collision_rect):
                game_over = True

        for saw in saws:

            collision_radius = saw["radius"] + 8

            saw_rect = pygame.Rect(
                saw["x"] - collision_radius,
                GROUND_Y - collision_radius,
                collision_radius * 2,
                collision_radius
            )

            if player.colliderect(saw_rect):
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

                if gem_count >= 1:
                    unlock_achievement("first_bloom")
 
                if gem_count >= 10:
                    unlock_achievement("gem_collector")

                # increase combo
                combo += 1
                combo_timer = COMBO_DURATION

                if combo >= 5:
                    unlock_achievement("combo_starter")

                # calculate combo bonus
                combo_bonus = combo * 10
                score += combo_bonus

        # Score and speed
        score += 1

        if score >= 1000:
            unlock_achievement("high_scorer")

        high_score = max(high_score, score)

        game_speed = min(
            10,
            5 + score // 1000
        )
    
    # update jump  trail particles
    for particle in jump_trail:

        particle["x"] -= game_speed
        particle["life"] -= 1
        particle["size"] *= 0.94
    
    jump_trail[:] = [
        p for p in jump_trail
        if p["life"] > 0
    ]

    # update combo timer
    if combo_timer > 0:
        combo_timer -= 1

        if combo_timer <= 0:
            combo = 0
            combo_bonus = 0
    
    #update achievement notifications
    for notification in achievement_notifications:
        notification["timer"] -= 1

    achievement_notifications[:] = [
        notification
        for notification in achievement_notifications
        if notification["timer"] > 0
    ]

    # update landing particles
    for particle in landing_particles:
        particle["x"] -= game_speed
        particle["y"] -= 0.5
        particle["life"] -= 1
        particle["size"] *= 0.94

    landing_particles[:] = [
        p for p in landing_particles
        if p["life"] > 0
    ]

    # update death particles

    if game_over and not death_effect_started:

        create_death_effect()
        death_effect_started = True

    for particle in death_particles:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["vy"] += 0.15
        particle["life"] -= 1
        particle["size"] *= 0.96

    death_particles[:] = [
        p for p in death_particles
        if p["life"] > 0
    ]

    if game_over and death_effect_started and shockwave_alpha > 0:
        shockwave_radius += 5
        shockwave_alpha = max(0, shockwave_alpha - 8)

    if game_over:
        game_over_alpha = min(255, game_over_alpha + 8)

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

        if obstacle["type"] == "hanging_spike":

           ceiling_points = [
               (rect.left - 55, rect.top - 35),
               (rect.left - 45, rect.top - 55),
               (rect.left - 15, rect.top - 62),
               (rect.centerx - 5, rect.top - 48),
               (rect.right + 20, rect.top - 60),
               (rect.right + 48, rect.top - 42),
               (rect.right + 55, rect.top - 20),
               (rect.right + 25, rect.top - 12),
               (rect.right + 12, rect.top),
               (rect.left - 12, rect.top),
               (rect.left - 30, rect.top - 12)
           ]

           pygame.draw.polygon(
               screen,
               DARK_PURPLE,
               ceiling_points
           )

           pygame.draw.polygon(
               screen,
               PURPLE,
               ceiling_points,
               3
           )

           pygame.draw.line(
               screen,
               NEON_PURPLE,
               (rect.left - 12, rect.top - 2),
               (rect.right + 12, rect.top - 2),
               2
           )

           points = [
               (rect.left, rect.top),
               (rect.right, rect.top),
               (rect.centerx, rect.bottom)
           ]

           draw_polygon_glow(screen, points, PINK)

           pygame.draw.polygon(
               screen,
               WHITE,
               points,
               2
           )

        elif obstacle["type"] == "spike":

            pygame.draw.polygon(
                screen,
                (8, 5, 25),
                [
                    (rect.left - 4, rect.bottom + 3),
                    (rect.centerx, rect.top - 4),
                    (rect.right + 4, rect.bottom + 3)
                ]
            )

            pygame.draw.polygon(
                screen,
                (100, 35, 180),
                [
                    (rect.left, rect.bottom),
                    (rect.centerx, rect.top),
                    (rect.right, rect.bottom)
                ]
            )

            pygame.draw.polygon(
                screen, 
                (255, 65, 180),
                [
                    (rect.left + 8, rect.bottom - 4),
                    (rect.centerx, rect.top + 12),
                    (rect.right - 8, rect.bottom - 4)
                ]
            )

            pygame.draw.polygon(
                screen,
                (80, 230, 255),
                [
                    (rect.left + 15, rect.bottom - 7),
                    (rect.centerx, rect.top + 20),
                    (rect.right - 15, rect.bottom - 7)
                ]
            )

            draw_polygon_glow(
                screen,
                [
                    (rect.left, rect.bottom),
                    (rect.centerx, rect.top),
                    (rect.right, rect.bottom)
                ],
                (180, 65, 255)
            )

        elif obstacle["type"] == "block":

            shadow_rect = rect.move(4, 4)

            pygame.draw.rect(
                screen, (8, 5, 25),
                shadow_rect, border_radius=4
            )

            pygame.draw.rect(
                screen, (75, 25, 130),
                rect, border_radius=4
            )

            pygame.draw.rect(
                screen, (180, 65, 255),
                rect, width=4, border_radius=4
            )

            stripe_spacing = 15

            for x in range(rect.left + 8, rect.right - 5, stripe_spacing):

                pygame.draw.line(
                    screen,
                    (80, 230, 255),
                    (x, rect.top + 7),
                    (x + 9, rect.bottom - 7),
                    3
                )

        elif obstacle["type"] == "moving_block":

            pygame.draw.rect(
                screen, DARK_PURPLE,
                rect, border_radius=5
            )

            pygame.draw.rect(
                screen, CYAN,
                rect, width=3, border_radius=5
            )

            inner_rect = rect.inflate(-12, 12)

            pygame.draw.rect(
                screen, (90, 45, 150),
                inner_rect, width=2, border_radius=3
            )

            cx, cy = rect.center

            diamond_points = [
                (cx, cy - 9),
                (cx + 9, cy),
                (cx, cy + 9),
                (cx - 9, cy)
            ]

            pygame.draw.polygon(screen, PINK, diamond_points)
            pygame.draw.polygon(screen, WHITE, diamond_points, 2)

# draw saws
    for saw in saws:

        if saw["grounded"]:
            screen.set_clip(
                pygame.Rect(0, 0, WIDTH, GROUND_Y)
            )

        draw_saw(
            screen,
            saw["x"],
            saw["y"],
            saw["radius"],
            saw["angle"]
        )

        screen.set_clip(None)

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

    # draw jump orbs

    for orb in jump_orbs:

        rect = orb["rect"]
        pulse = math.sin(orb["pulse"]) * 3

        center = rect.center

        pygame.draw.circle(
            screen,
            (35, 100, 150),
            center,
            int(23 + pulse)
        )

        #main orb
        pygame.draw.circle(
            screen,
            CYAN,
            center,
            14
        )

        pygame.draw.circle(
            screen,
            WHITE,
            center,
            14,
            3
        )

        pygame.draw.circle(
            screen,
            NEON_CYAN,
            center,
            6
        )

    #draw jump pads
    for pad in jump_pads:
        pygame.draw.rect(
            screen,
            DARK_PURPLE,
            pad,
            border_radius=5
        )

        pygame.draw.rect(
            screen,
            NEON_PURPLE,
            pad,
            3,
            border_radius=5
        )

        pygame.draw.line(
            screen,
            PINK,
            (pad.left + 8, pad.top + 3),
            (pad.right - 8, pad.top + 3),
            3
        )

        pygame.draw.circle(
            screen,
            WHITE,
             pad.center,
            3
        )
    
    
    # draw jump trail
    for particle in jump_trail:

        alpha = int(
            255 * particle["life"] / particle["max_life"]
        )

        size = max(1, int(particle["size"]))

        trail_surface = pygame.Surface(
            (size * 4, size * 4),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            trail_surface,
            (*particle["color"], alpha),
            (size * 2, size * 2),
            size
        )

        screen.blit(
            trail_surface,
            (
                int(particle["x"] - size * 2),
                int(particle["y"] - size * 2)
            )
        )

    #draw landing particles
    for particle in landing_particles:

        alpha = int(
            255 * particle["life"] / particle["max_life"]
        )

        size = max(1, int(particle["size"]))

        landing_surface = pygame.Surface(
            (size * 4, size * 4),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            landing_surface,
            (*particle["color"], alpha),
            (size * 2, size * 2),
            size
        )

        screen.blit(
            landing_surface,
            (
                int(particle["x"] - size * 2),
                int(particle["y"] - size * 2)
            )
        )



    # ======================================
    # DRAW PLAYER
    # ======================================

    # create animation

    animated_width = int(PLAYER_WIDTH * player_scale_x)
    animated_height = int(PLAYER_HEIGHT * player_scale_y)

    animated_width = max(1, animated_width)
    animated_height = max(1, animated_height)

    cube_surface = pygame.Surface(
        (animated_width, animated_height),
        pygame.SRCALPHA
    )

    #Main cube

    pygame.draw.rect(
        cube_surface,
        NEON_PURPLE,
        (0, 0, animated_width, animated_height),
        border_radius=5
    )

    pygame.draw.rect(
        cube_surface,
        NEON_CYAN,
        (0, 0, animated_width, animated_height),
        3,
        border_radius=5
    )

    pygame.draw.rect(
        cube_surface,
        PINK,
        (
            animated_width // 4,
            animated_height // 4,
            animated_width // 2,
            animated_height // 2
        ),
        2
    )

    rotated_cube = pygame.transform.rotate(
        cube_surface,
        cube_angle
    )

    cube_rect = rotated_cube.get_rect(
        center=player.center
    )

    screen.blit(rotated_cube, cube_rect)



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

    combo_text = small_font.render(
        f"COMBO: x{combo}",
        True,
        CYAN if combo > 1 else WHITE
    )

    screen.blit(score_text, (25, 80))

    if combo > 1:
        screen.blit(combo_text, (20, 50))

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

    #==================================
    # ACHIEVEMENT NOTIFICATION
    #==================================

    if achievement_notifications and not game_over:

        notification = achievement_notifications[-1]

        notification_surface = pygame.Surface(
            (329, 85),
            pygame.SRCALPHA
        )

        #Panel background
        pygame.draw.rect(
            notification_surface,
            (25, 12, 55, 230),
            (0, 0, 320, 85),
            border_radius=12
        )

        #glowing border
        pygame.draw.rect(
            notification_surface,
            CYAN,
            (0, 0, 320, 85),
            3,
            border_radius=12
        )

        #heading
        heading = small_font.render(
            "ACHIEVEMENT UNLOCKED!",
            True,
            PINK
        )

        # Achievement name
        name = achievement_font.render(
            notification["name"],
            True,
            WHITE
        )

        # description
        description = small_font.render(
            notification["description"],
            True,
            CYAN
        )

        notification_surface.blit(heading, (15, 10))
        notification_surface.blit(name, (15, 32))
        notification_surface.blit(description, (15, 60))

        screen.blit(
            notification_surface,
            (WIDTH - 340, 25)
        )

    #=====================================
    # ACHIEVEMENT COLLECTION
    # ===================================

    if show_achievements:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(210)
        overlay.fill((10, 5, 30))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(190, 65, 520, 370)

        pygame.draw.rect(
            screen,
            DARK_PURPLE,
            panel,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            CYAN,
            panel,
            3,
            border_radius=18
        )

        heading = title_font.render(
            "ACHIEVEMENTS",
            True,
            PINK
        )

        screen.blit(
            heading,
            heading.get_rect(center=(WIDTH // 2, 105))
        )

        y_position = 145

        progress_values = {
            "first_bloom": f"{min(gem_count, 1)}/1 gems",
            "gem_collector": f"{min(gem_count, 10)}/10 gems",
            "combo_starter": f"{min(combo, 5)}/5 combo",
            "high_scorer": f"{min(score, 1000)}/1000 points"
        }

        for achievement_id, achievement in achievements.items():
            if achievement["unlocked"]:
                status = "UNLOCKED"
                status_color = CYAN

            else:
                status = "LOCKED"
                status_color = (130, 120, 150)

            name_text = achievement_font.render(
                achievement["name"],
                True,
                WHITE
            )

            description_text = small_font.render(
                achievement["description"],
                True,
                (190, 180, 210)
            )

            progress_text = small_font.render(
                progress_values[achievement_id],
                True,
                CYAN
            )

            # achievement progress bar
            progress_amounts = {
                "first_bloom": min(gem_count / 1, 1),
                "gem_collector": min(gem_count / 10, 1),
                "combo_starter": min(combo / 5, 1),
                "high_scorer": min(score / 1000, 1)
            }

            bar_x = 430
            bar_y = y_position + 48
            bar_width = 180
            bar_height = 8

            pygame.draw.rect(
                screen,
                (65, 55, 90),
                (bar_x, bar_y, bar_width, bar_height),
                border_radius=5
            )

            pygame.draw.rect(
                screen,
                CYAN,
                (
                    bar_x,
                    bar_y,
                    int(bar_width * progress_amounts[achievement_id]),
                    bar_height
                ),
                border_radius=5
            )

            status_text = small_font.render(
                status,
                True,
                status_color
            )

            screen.blit(name_text, (225, y_position))
            screen.blit(description_text, (225, y_position + 27))

            screen.blit(progress_text, (225, y_position + 45))

            screen.blit(
                status_text,
                status_text.get_rect(
                    midright=(675, y_position + 15)
                )
            )

            y_position += 60

        close_text = small_font.render(
            "Press A to close",
            True,
            CYAN
        )

        screen.blit(
            close_text,
            close_text.get_rect(
                center=(WIDTH // 2, 405)
            )
        )

    # ======================================
    # GAME OVER
    # ======================================

    if game_over:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(int(180 * game_over_alpha / 255))
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

        final_score = small_font.render(
            f"Final Score: {score}",
            True,
            CYAN
        )

        final_gems = small_font.render(
            f"Gems Collected: {gem_count}",
            True,
            YELLOW
        )

        message.set_alpha(game_over_alpha)
        restart.set_alpha(game_over_alpha)

        final_score.set_alpha(game_over_alpha)
        final_gems.set_alpha(game_over_alpha)

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

        screen.blit(
            final_score,
            final_score.get_rect(
                 center=(WIDTH // 2, HEIGHT // 2 + 75)
            )
        )

        screen.blit(
            final_gems,
            final_gems.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 110)
            )
        )

    #draw death shockwave
    if game_over and shockwave_alpha > 0:

        shockwave_surface = pygame.Surface(
            (shockwave_radius * 2 + 10, shockwave_radius * 2 + 10),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            shockwave_surface,
            (*CYAN, shockwave_alpha),
            (shockwave_radius + 5, shockwave_radius + 5),
            shockwave_radius,
            3
        )

        screen.blit(
            shockwave_surface,
            (
                player.centerx - shockwave_radius - 5,
                player.centery - shockwave_radius - 5
            )
        )


    # draw death particles

    for particle in death_particles:

        alpha = int(
            255 * particle["life"] / particle["max_life"]
        )

        size = max(1, int(particle["size"]))

        particle_surface = pygame.Surface(
            (size * 6, size * 6),
            pygame.SRCALPHA
        )

        center = (size * 3, size * 3)

        pygame.draw.circle(
            particle_surface,
            (*particle["color"], alpha // 5),
            center,
            size * 3
        )

        pygame.draw.circle(
            particle_surface,
            (*particle["color"], alpha // 2),
            center,
            size * 2
        )

        pygame.draw.circle(
            particle_surface,
            (*particle["color"], alpha),
            center,
            size
        )

        screen.blit(
            particle_surface,
            (
                int(particle["x"] - size * 3),
                int(particle["y"] - size * 3)
            )
        )

    #=========================================
    # MAIN MENU
    #========================================

    if game_state == MENU:

        menu_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )
        menu_overlay.fill((10, 5, 30, 225))
        screen.blit(menu_overlay, (0, 0))

        #Game title
        menu_title = title_font.render(
            "ROSAS RUSH",
            True,
            PINK
        )

        screen.blit(
            menu_title,
            menu_title.get_rect(
                center=(WIDTH // 2, 145)
            )
        )

        #subtitle
        subtitle = small_font.render(
            "A NEON FOREST ADVENTURE",
            True,
            CYAN
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(WIDTH // 2, 195)
            )
        )

        #menu options
        play_text = achievement_font.render(
            "PRESS ENTER TO PLAY",
            True,
            WHITE
        )

        help_text = small_font.render(
            "H - HOW TO PLAY",
            True,
            CYAN
        )

        quit_text = small_font.render(
            "ESC - QUIT GAME",
            True,
            PINK
        )

        screen.blit(
            play_text,
            play_text.get_rect(
                center=(WIDTH // 2, 290)
            )
        )

        screen.blit(
            help_text,
            help_text.get_rect(
                center=(WIDTH // 2, 340)
            )
        )

        screen.blit(
            quit_text,
            quit_text.get_rect(
                center=(WIDTH // 2,  375)
            )
        )

        #========================================
        # HOW TO PLAY SCREEN
        #==========================================

    elif game_state == HOW_TO_PLAY:
        menu_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        menu_overlay.fill((10, 5, 30, 235))
        screen.blit(menu_overlay, (0, 0))

        heading = title_font.render(
            "HOW TO PLAY",
            True,
            PINK
        )

        screen.blit(
            heading,
            heading.get_rect(
                center=(WIDTH // 2, 105)
            )
        )

        instructions = [
            ("SPACE", "Jump"),
            ("SPACE", "Activate jump orbs"),
            ("COLLECT", "Gather gems and roses"),
            ("AVOID", "Spikes, saws, and gaps"),
            ("A", "View achievements")
             
        ]

        y_position = 180

        for control, description in instructions:

            control_text = achievement_font.render(
                control,
                True,
                CYAN
            )

            description_text = small_font.render(
                description,
                True,
                WHITE
            )

            screen.blit(
                control_text,
                (230, y_position)
            )

            screen.blit(
                description_text,
                (410, y_position + 3)
            )

            y_position += 42

        back_text = small_font.render(
            "PRESS ESC TO RETURN",
            True,
            PINK
        )

        screen.blit(
            back_text,
            back_text.get_rect(
                center=(WIDTH // 2, 440)
            )
        )

    pygame.display.flip()

pygame.quit()