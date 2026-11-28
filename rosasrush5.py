import pygame
import random
import math
import json
import os

pygame.init()

WIDTH = 900
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rosas Rush")
clock = pygame.time.Clock()

# GAME STATES

MENU = "menu"
PLAYING = "playing"
HOW_TO_PLAY = "how_to_play"
STATISTICS = "statistics"
WELCOME = "welcome"
CONFIRM_RESET = "confirm_reset"
SHOP = "shop"
LEVEL_SELECT = "level_select"
LEVEL_COMPLETE = "level_complete"

game_state = MENU

pause_menu_active = False

coin_balance = 0
coins_collected = 0
coins = []

#shop sys
equipped_cube = "Classic Cube"
equipped_trail = None
equipped_death_effect = None

trail_particles = []
TRAIL_SPAWN_DELAY = 3
trail_timer = 0

shop_category = "CUBES"

shop_categories = [
    "CUBES",
    "TRAILS",
    "DEATH EFFECTS"
]

shop_scroll = 0

shop_items = {
    "CUBES": [
        {"name": "Classic Cube", "price": 0},
        {"name": "Rose Cube", "price": 25},
        {"name": "Neon Cube", "price": 50}
    ],

    "TRAILS": [
        {"name": "Pink Trail", "price": 30},
        {"name": "Cyan Trail", "price": 40},
        {"name": "Rainbow Trail", "price": 60}
    ],

    "DEATH EFFECTS": [
        {"name": "Rose Burst", "price":35},
        {"name": "Star Burst", "price": 45},
        {"name": "Neon Burst", "price": 60}
    ]
}

owned_items = ["Classic Cube"]

shop_item_buttons = [
    pygame.Rect(115, 325, 190, 48),
    pygame.Rect(355, 325, 190, 48),
    pygame.Rect(595, 325, 190, 48)
]

shop_notice = ""
shop_notice_timer = 0
selected_shop_item = None


# COLORS

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
GREEN = (100, 255, 150)

GOLD = (255, 200, 50)
LIGHT_GOLD = (255, 235, 130)

COIN_SIZE = 22
COIN_SPAWN_CHANCE = 0.65

ROSE_CUBE_MAIN = (220, 65, 110)
ROSE_CUBE_OUTLINE =(225, 170, 195)

NEON_CUBE_MAIN = (80, 230, 255)
NEON_CUBE_OUTLINE = (180, 100, 255)

RAINBOW_COLORS = [
    (255, 80, 140),
    (255, 180, 70),
    (255, 240, 90),
    (80, 255, 180),
    (80, 200, 255),
    (180, 100, 255)
]
# FONTS

title_font = pygame.font.SysFont("bahnschrift", 72, bold=True)
small_font = pygame.font.SysFont("bahnschrift", 24)
achievement_font = pygame.font.SysFont("bahnschrift", 32, bold=True)
button_font = pygame.font.SysFont("bahnschrift", 21, bold=True)
hud_title_font = pygame.font.SysFont("bahnschrift", 32, bold=True)
how_title_font = pygame.font.SysFont("bahnschrift", 46, bold=True)
instruction_font = pygame.font.SysFont("bahnschrift", 19, bold=True)
welcome_input_font = pygame.font.SysFont("bahnschrift", 19)
welcome_title_font = pygame.font.SysFont("bahnschrift", 42, bold=True)
welcome_subtitle_font = pygame.font.SysFont("bahnschrift", 25, bold=True)
welcome_text_font = pygame.font.SysFont("bahnschrift", 18)

# MENU BUTTONS

play_button = pygame.Rect(340, 175, 220, 42)
help_button = pygame.Rect(340, 225, 220, 42)
achievements_button = pygame.Rect(340, 275, 220, 42)
shop_button = pygame.Rect(340, 325, 220, 42)
quit_button = pygame.Rect(340, 375, 220, 42)

level_buttons = [
    pygame.Rect(90, 190, 220, 190),
    pygame.Rect(340, 190, 220, 190),
    pygame.Rect(590, 190, 220, 190)
]

level_back_button = pygame.Rect(
    WIDTH - 135,
    HEIGHT - 62,
    110,
    42
)

level_complete_button = pygame.Rect(
    330,
    365,
    240,
    48
)

cube_category_button = pygame.Rect(130, 205, 190, 50)
trail_category_button = pygame.Rect(355, 205, 190, 50)
death_category_button = pygame.Rect(580, 205, 190, 50)

stats_button = pygame.Rect(24, 24, 52, 52)
back_button = pygame.Rect(340, 420, 220, 50)
reset_data_button = pygame.Rect(650, 420, 160, 40)
confirm_reset_button = pygame.Rect(250, 270, 180, 50)
cancel_reset_button = pygame.Rect(470, 270, 180, 50)

resume_button = pygame.Rect(340, 185, 220, 48)
restart_button = pygame.Rect(340, 250, 220, 48)
pause_menu_button = pygame.Rect(340, 315, 220, 48)
pause_quit_button = pygame.Rect(340, 380, 220, 48)
pause_button = pygame.Rect(815, 20, 60, 50)

#wc screen buttons
welcome_input_box = pygame.Rect(250, 245, 400, 55)
continue_button = pygame.Rect(340, 330, 220, 55)

# stats name edit
edit_name_button = pygame.Rect(650, 125, 130, 40)
save_name_button = pygame.Rect(650, 125, 130, 40)
stats_name_box = pygame.Rect(180, 125, 450, 40)
stats_scroll = 0
stats_scroll_speed = 25
stats_content_height = 520
stats_scroll_limit = 0
stats_viewport = pygame.Rect(70, 65, 760, 345)

# player name settings
player_name = ""
name_input_text =""
editing_name = False

button_scales = {}

click_effect_pos = None
click_effect_time = 0

last_screen = None
page_fade_alpha = 0
PAGE_FADE_SPEED = 12

# 1st time tut

tutorial_active = False
tutorial_step = 0
tutorial_completed = False

tutorial_pause_opened = False
tutorial_pause_resumed = False

game_tutorial_active = False
game_tutorial_completed = False
game_tutorial_step = 0

game_tutorial_skip_button = pygame.Rect(730, 25, 140, 42)
game_tutorial_replay_button = pygame.Rect(600, 420, 250, 45)

tutorial_orb_used = False
tutorial_pad_used = False
tutorial_gem_collected = False
tutorial_rose_collected = False
tutorial_finished = False

skip_tutorial_button = pygame.Rect(730, 25, 140, 42)

tutorial_targets = [
    play_button,
    help_button,
    achievements_button,
    stats_button
]

tutorial_titles = [
    "LET'S PLAY!",
    "NEED SOME HELP?",
    "YOUR ACHIEVEMENTS",
    "TRACK YOUR PROGRESS"
]

tutorial_messages = [
    "Click here whenever you're ready to start a run!",
    "Learn the controls and how to play Rosas Rush.",
    "Complete challenges and unlock achievements!",
    "Check your statistics and personal records here."
]

def draw_button(rect, text, mouse_pos):

    global click_effect_pos, click_effect_time

    hovered = rect.collidepoint(mouse_pos)
    button_key = (text, rect.x, rect.y, rect.width, rect.height)

    current_scale = button_scales.get(button_key, 1.0)
    target_scale = 1.05 if hovered else 1.0
    current_scale += (target_scale - current_scale) * 0.2

    button_scales[button_key] = current_scale

    if (
        click_effect_pos is not None
        and rect.collidepoint(click_effect_pos)
        and pygame.time.get_ticks() - click_effect_time < 130
    ):
        current_scale *= 0.94

    animated_width = int(rect.width * current_scale)
    animated_height = int(rect.height * current_scale)

    animated_rect = pygame.Rect(
        0, 0, animated_width, animated_height
    )

    animated_rect.center = rect.center

    if hovered:
        button_color = (85, 40, 130)
        border_color = CYAN
        text_color = (255, 255, 255)

    else:
        button_color = (38, 22, 75)
        border_color = (175, 85, 190)
        text_color = (255, 215, 245)

    shadow_rect = animated_rect.move(0, 4)

    pygame.draw.rect(
        screen,
        (12, 7, 30),
        shadow_rect,
        border_radius=14
    )

    if hovered:
        glow_rect = animated_rect.inflate(14, 14)

        pygame.draw.rect(
            screen, 
            (65, 35, 110),
            glow_rect,
            border_radius=18
        )

    pygame.draw.rect(
        screen,
        button_color,
        animated_rect,
        border_radius=13
    )

    pygame.draw.rect(
        screen,
        border_color,
        animated_rect,
        2,
        border_radius=13
    )

    inner_rect = animated_rect.inflate(-8, -8)
    if inner_rect.width > 0 and inner_rect.height > 0:
        pygame.draw.rect(
            screen,
            (100, 65, 145),
            inner_rect,

            1,
            border_radius=9
        )

    if text == "ACHIEVEMENTS":
        button_text = pygame.font.SysFont(
            "bahnschrift", 18, bold=True
        ).render(text, True, text_color)

    else:
        button_text = button_font.render(
            text,
            True,
            text_color
        )

    screen.blit(
        button_text,
        button_text.get_rect(center=animated_rect.center)
    )


def draw_pause_button(rect, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)

    button_color = (100, 45, 155) if hovered else (35, 20, 70)

    pygame.draw.rect(
        screen,
        button_color,
        rect,
        border_radius=12
    )

    border_color = CYAN if hovered else PINK

    pygame.draw.rect(
        screen,
        border_color,
        rect,
        2,
        border_radius=12
    )

    bar_color = (255, 160, 210) if hovered else PINK

    bar_width = 6
    bar_height = 20
    gap = 7

    center_x, center_y = rect.center

    left_bar = pygame.Rect(
        center_x - gap // 2 - bar_width,
        center_y - bar_height // 2,
        bar_width,
        bar_height
    )

    right_bar = pygame.Rect(
        center_x + gap // 2,
        center_y - bar_height // 2,
        bar_width,
        bar_height
    )

    pygame.draw.rect(
        screen,
        bar_color,
        left_bar,
        border_radius=3
    )

    pygame.draw.rect(
        screen,
        bar_color,
        right_bar,
        border_radius=3
    )

def draw_tutorial_overlay():

    target = tutorial_targets[tutorial_step]

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((8, 4, 25, 190))

    spotlight = target.inflate(18, 18)

    pygame.draw.rect(
        overlay,
        (0, 0, 0, 0),
        spotlight,
        border_radius=15
    )

    screen.blit(overlay, (0, 0))

    pygame.draw.rect(
        screen,
        CYAN,
        spotlight,
        3,
        border_radius=15
    )

    arrow_start = (
        spotlight.centerx + 55,
        spotlight.bottom + 65
    )

    arrow_end = (
        spotlight.centerx + 8,
        spotlight.bottom + 8
    )

    pygame.draw.line(
        screen, PINK, arrow_start, arrow_end, 5
    )

    pygame.draw.polygon(
        screen,
        PINK,
        [
            arrow_end,
            (arrow_end[0] + 15, arrow_end[1] + 3),
            (arrow_end[0] + 5, arrow_end[1] + 15)
        ]
    )

    card = pygame.Rect(140, 385, 620, 95)

    pygame.draw.rect(
        screen,
        DARK_PURPLE,
        card,
        border_radius=15
    )

    pygame.draw.rect(
        screen, 
        PINK,
        card,
        2,
        border_radius=15
    )

    title = achievement_font.render(
        tutorial_titles[tutorial_step],
        True,
        CYAN
    )

    screen.blit(
        title,
        (card.x + 22, card.y + 12)
    )

    message = small_font.render(
        tutorial_messages[tutorial_step],
        True,
        WHITE
    )

    screen.blit(
        message,
        (card.x + 22, card.y + 55)
    )

    draw_button(
        skip_tutorial_button,
        "SKIP",
        pygame.mouse.get_pos()
    )

def start_game_tutorial():

    global game_tutorial_active, game_tutorial_step
    global game_over, show_achievements
    global player, player_y, player_velocity
    global on_ground, game_speed
    global tutorial_orb_used, tutorial_pad_used
    global tutorial_gem_collected, tutorial_rose_collected
    global tutorial_finished
    global tutorial_pause_opened, tutorial_pause_resumed
    global trail_particles

    trail_timer = 0

    game_tutorial_active = True
    game_tutorial_step = 0

    tutorial_pause_opened = False
    tutorial_pause_resumed = False

    tutorial_orb_used = False
    tutorial_pad_used = False
    tutorial_gem_collected = False
    tutorial_rose_collected = False
    tutorial_finished = False

    game_over = False
    show_achievements = False

    player = pygame.Rect(
        PLAYER_X,
        GROUND_Y - PLAYER_HEIGHT,
        PLAYER_WIDTH,
        PLAYER_HEIGHT
    )

    player_y = float(player.y)
    player_velocity = 0
    on_ground = True

    game_speed = 4

    platforms.clear()
    trail_particles.clear()
    trial_timer = 0
    gaps.clear()
    obstacles.clear()
    gems.clear()
    roses.clear()
    jump_orbs.clear()
    jump_pads.clear()
    saws.clear()

    obstacles.append({
        "rect": pygame.Rect(
            650,
            GROUND_Y - 35,
            35,
            35
        ),
        "type": "spike"
    })

    gems.append(
        pygame.Rect(850, 300, 28, 28)
    )

    roses.append(
        pygame.Rect(1100, GROUND_Y - 35, 25, 30)
    )

    jump_orbs.append({
        "rect": pygame.Rect(1400, 285, 30, 30),
        "pulse": 0
    })

    jump_pads.append(
        pygame.Rect(1700, GROUND_Y - 12, 50, 12)
    )

# DRAW STATS ICON
def draw_stats_icon(rect, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    icon_color = CYAN if hovered else PINK

    pygame.draw.circle(
        screen,
        (55, 25, 95),
        rect.center,
        27
    )

    pygame.draw.circle(
        screen, 
        icon_color,
        rect.center,
        27,
        2
    )

    bar_width = 5

    bars = [
        (rect.x + 13, rect.y + 28, 7, 12),
        (rect.x + 23, rect.y + 20, 7, 20),
        (rect.x + 33, rect.y + 12, 7, 28)
    ]

    for x, y, width, height in bars:

        pygame.draw.rect(
            screen,
            icon_color,
            (x, y, width, height),
            border_radius=2
        )

# BACKGROUND SETTINGS
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

# MAIN MENU BG EFFECTS
menu_sparkles = []
for _ in range(35):

    menu_sparkles.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "size": random.randint(1, 3),
        "speed": random.uniform(0.2, 0.7),
        "phase": random.uniform(0, 6.28),
        "color": random.choice([
            (255, 125, 180),
            (150, 60, 255),
            (210, 170, 255)
        ])
    })

menu_glow = pygame.Surface(
(WIDTH, HEIGHT),
pygame.SRCALPHA
)

pygame.draw.circle(
menu_glow,
(100, 35, 180, 12),
(WIDTH // 2, 245),
300
)

pygame.draw.circle(
menu_glow,
(150, 50, 220, 14),
(WIDTH // 2, 245),
230
)

pygame.draw.circle(
menu_glow,
(220, 65, 150, 12),
(WIDTH // 2, 245),
160
)

menu_vignette = pygame.Surface(
(WIDTH, HEIGHT),
pygame.SRCALPHA
)

for i in range(12):

    inset_x = i * 8
    inset_y = i * 6

    pygame.draw.rect(
        menu_vignette,
        (5, 0, 20, 5),
        (
            inset_x,
            inset_y,
            WIDTH - inset_x * 2,
            HEIGHT - inset_y * 2
        ),
        width=8
    )

# LEVEL SETTINGS
GROUND_Y = 430
PLAYER_X = 140
PLAYER_WIDTH = 35
PLAYER_HEIGHT = 40
GRAVITY = 0.7
JUMP_STRENGTH = -15

# PLAYER
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

# LEVEL OBJECTS 
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

    "high_scorer": {
        "name": "High Scorer",
        "description": "Reach 1,000 points",
        "unlocked": False
    },

    "gem_hoarder": {
        "name": "Gem Hoarder",
        "description": "Collect 50 gems total",
        "unlocked": False
    },

    "rose_keeper": {
        "name": "Rose Keeper",
        "description": "Collect 20 roses total",
        "unlocked": False
    },

    "combo_master": {
        "name": "Combo Master",
        "description": "Reach a 10x combo",
        "unlocked": False
    },

    "first_flight": {
        "name": "First Flight",
        "description": "Activate jump orbs 5 times",
        "unlocked": False
    },

    "dedicated_player": {
        "name": "Dedicated Player",
        "description": "Play 20 runs",
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
        save_data()
# LEVL PROGRESSION SYSTEM

levels = {
    1: {
        "name": "FIRST STEPS",
        "difficulty": "EASY",
        "description": "A beginner-friendly adventure.",
        "speed": 5,
        "target_score": 1800,
        "obstacle_frequency": (650, 850),
        "unlocked": True

    },

    2: {
        "name": "NEON PATH",
        "difficulty": "NORMAL",
        "description": "A faster journey through the neon forest.",
        "speed": 6,
        "target_score": 3000,
        "obstacle_frequency": (500, 700),
        "unlocked": False
    },

    3: {
        "name": "ROSE RUSH",
        "difficulty": "HARD",
        "description": "Only the best can conquer this challenge.",
        "speed": 7,
        "target_score": 4500,
        "obstacle_frequency": (400, 600),
        "unlocked": False

    }
}

selected_level = 1
unlocked_levels = [1]
completed_levels = []

# GAME SETTINGS
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

# SAVE AND LOAD GAME DATA
total_gems = 0
total_roses = 0
total_orb_activations = 0
runs_completed = 0
best_combo = 0
best_survival_time = 0
run_start_ticks = None
pause_started_ticks = None

SAVE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "rosas_rush_data.json"
)

def equip_shop_item(item_name, category):

    global equipped_cube
    global equipped_trail
    global equipped_death_effect

    if item_name not in owned_items:
        return

    if category == "CUBES":
        equipped_cube = item_name

    elif category == "TRAILS":
        equipped_trail = item_name

    elif category == "DEATH EFFECTS":
        equipped_death_effect = item_name
    save_data()

def load_data():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, dict):
                return data

    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass

    return{}

def save_data():

    data = {
        "player_name": player_name,
        "high_score": high_score,
        "total_gems": total_gems,
        "total_roses": total_roses,
        "total_orb_activations": total_orb_activations,
        "runs_completed": runs_completed,
        "best_combo": best_combo,
        "best_survival_time": best_survival_time,
        "tutorial_completed": tutorial_completed,
        "game_tutorial_completed": game_tutorial_completed,
        "coin_balance": coin_balance,
        "owned_items": owned_items,
        "equipped_cube": equipped_cube,
        "equipped_trail": equipped_trail,
        "equipped_death_effect": equipped_death_effect,
        "unlocked_levels": unlocked_levels,
        "completed_levels": completed_levels,

        "achievements": {
            achievement_id: achievement["unlocked"]
            for achievement_id, achievement in achievements.items()
        }
    }

    try:
        with open(SAVE_FILE, "w", encoding="utf=8") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print("Could not save game data:", error)

def complete_level():  
    global game_state

    #remember the comple level
    if selected_level not in completed_levels:
        completed_levels.append(selected_level)

    #unlock next lev
    next_level = selected_level + 1

    if next_level in levels:
        if next_level not in unlocked_levels:
            unlocked_levels.append(next_level)

    save_data()

    game_state = LEVEL_COMPLETE

def reset_saved_data():

    global equipped_cube
    global equipped_trail
    global equipped_death_effect

    global game_tutorial_completed
    global player_name
    global name_input_text
    global high_score
    global total_gems, total_roses
    global total_orb_activations
    global runs_completed, best_combo
    global best_survival_time
    global tutorial_completed
    global coin_balance
    global owned_items
    global unlocked_levels
    global completed_levels

    tutorial_completed = False
    game_tutorial_completed = False

    player_name = ""
    name_input_text = ""

    owned_items = ["Classic Cube"]

    equipped_cube = "Classic Cube"
    equipped_trail = None
    equipped_death_effect = None

    high_score = 0
    total_gems = 0
    total_roses = 0
    total_orb_activations = 0
    runs_completed = 0
    best_combo = 0
    best_survival_time = 0
    coin_balance = 0 

    unlocked_levels = [1]
    completed_levels = []

    for achievement in achievements.values():
        achievement["unlocked"] = False

    achievement_notifications.clear()
    save_data()
saved_data = load_data()

tutorial_completed = saved_data.get("tutorial_completed", False)
game_tutorial_completed = saved_data.get(
    "game_tutorial_completed", False
)
high_score = saved_data.get("high_score", 0)
total_gems = saved_data.get("total_gems", 0)
total_roses = saved_data.get("total_roses", 0)
total_orb_activations = saved_data.get("total_orb_activations", 0)
runs_completed = saved_data.get("runs_completed", 0)
best_combo = saved_data.get("best_combo", 0)
best_survival_time = saved_data.get("best_survival_time", 0)
coin_balance = saved_data.get("coin_balance", 0)

owned_items = saved_data.get("owned_items", ["Classic Cube"])


equipped_cube = saved_data.get("equipped_cube", "Classic Cube")
equipped_trail = saved_data.get("equipped_trail", None)
equipped_death_effect = saved_data.get("equipped_death_effect", None)

unlocked_levels = saved_data.get("unlocked_levels", [1])
completed_levels = saved_data.get("completed_levels", [])

if not isinstance(unlocked_levels, list):
    unlocked_levels = [1]

if not isinstance(completed_levels, list):
    completed_levels = []

if 1 not in unlocked_levels:
    unlocked_levels.append(1)

if not isinstance(owned_items, list):
    owned_items = ["Classic Cube"]


saved_achievements = saved_data.get("achievements", {})

for achievement_id in achievements:

    achievements[achievement_id]["unlocked"] = saved_achievements.get(
        achievement_id, False
    )

# load player name
player_name = saved_data.get("player_name", "").strip()

#show welcome screen
if player_name:
    game_state = MENU

    if not tutorial_completed:
        tutorial_active = True
        tutorial_step = 0
else:
    game_state = WELCOME

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

def create_trail_particle():
    if equipped_trail is None:
        return

    trail_color = PINK

    if equipped_trail == "Cyan Trail":
        trail_color = CYAN

    elif equipped_trail == "Rainbow Trail":
        trail_color = random.choice(RAINBOW_COLORS)

    trail_particles.append({
        "x": player.left,
        "y": player.centery,
        "radius": random.randint(3, 6),
        "color": trail_color,
        "life": 25
    })

def draw_star(surface, color, center, size):
    points = []

    for i in range(10):

        angle = math.radians(i * 36 - 90)

        if i % 2 == 0:
            radius = size
        else:
            radius = size * 0.45

        x = center[0] + math.cos(angle) * radius
        y = center[1] + math.sin(angle) * radius

        points.append((x, y))
    pygame.draw.polygon(surface, color, points)
    
def create_death_effect():

    global death_particles
    global shockwave_radius, shockwave_alpha

    shockwave_radius = 5
    shockwave_alpha = 225

    death_particles = []

    #choose de
    if equipped_death_effect == "Rose Burst":

        colors = [
            PINK,
            ROSE_RED,
            (255, 150, 190)
        ]

    elif equipped_death_effect == "Star Burst":
        colors = [
            (255, 230, 100),
            WHITE,
            (255, 180, 60)
        ]

    elif equipped_death_effect == "Neon Burst":

        colors = [
            CYAN,
            NEON_PURPLE,
            NEON_CYAN,

        ]

    else:
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
            "max_life": 45,
            "shape": "star" if equipped_death_effect == "Star Burst" else "circle"
        })

# DRAW BACKGROUND
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
# DRAW MAIN MENU ATMOSPHERE

def draw_menu_atmosphere():

    current_time = pygame.time.get_ticks()

    screen.blit(menu_glow, (0, 0))

    for particle in menu_sparkles:

        particle["y"] -= particle["speed"]

        particle["x"] += math.sin(
            current_time * 0.001 + particle["phase"]
        ) * 0.3

        if particle["y"] < -5:

            particle["y"] = HEIGHT + random.randint(5, 50)
            particle["x"] = random.randint(0, WIDTH)

        x = int(particle["x"])
        y = int(particle["y"])
        size = particle["size"]

        pygame.draw.circle(
            screen,
            (65, 35, 100),
            (x, y),
            size + 3
        )

        pygame.draw.circle(
            screen,
            particle["color"],
            (x, y),
            size
        )

    screen.blit(menu_vignette, (0, 0))

# DRAW LEVEL SELECT
def draw_level_select_screen():

    screen.fill(BACKGROUND)
    draw_menu_atmosphere()

    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()

    #screen title
    title = title_font.render(
        "SELECT YOUR LEVEL",
        True,
        PINK
    )

    screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, 85))
    )

    subtitle = small_font.render(
        "Choose your next adventure!",
        True,
        CYAN
    )

    screen.blit(
        subtitle, 
        subtitle.get_rect(
            center=(WIDTH // 2, 130)
        )
    )

    #level cards
    for index, level_number in enumerate(levels):
        level = levels[level_number]
        card = level_buttons[index]

        is_unlocked = level_number in unlocked_levels
        is_hovered = card.collidepoint(mouse_pos)

        #cardd colors
        if is_unlocked:
            card_color = (40, 20, 85)
            border_color = CYAN if is_hovered else PURPLE

        else:
            card_color = (25, 20, 45)
            border_solor = (75, 65, 95)

        #hover animation 
        pulse = abs(math.sin(current_time * 0.004)) * 2

        pygame.draw.rect(
            screen,
            card_color,
            card,
            border_radius = 18
        )

        pygame.draw.rect(
            screen,
            border_color,
            card,
            3,
            border_radius = 18
        )

        if is_unlocked and is_hovered:
            pygame.draw.rect(
                screen,
                CYAN,
                card.inflate(
                    int(pulse + 4),
                    int(pulse + 4)
                ),
                1,
                border_radius=20
            )

        #level number
        number_text = title_font.render(
            f"{level_number:02}",
            True,
            WHITE if is_unlocked else (100, 90, 115)
        )

        screen.blit(
            number_text,
            number_text.get_rect(
                center=(card.centerx, card.y + 45)
            )
        )

        #level name
        name_text = small_font.render(
            level["name"],
            True,
            PINK if is_unlocked else (110, 100, 125)
        )

        screen.blit(
            name_text,
            name_text.get_rect(
                center=(card.centerx, card.y + 90)
            )
        )

        #difficulty
        difficulty_colors = {
            "EASY": GREEN,
            "NORMAL": GOLD,
            "HARD": ROSE_RED
        }

        difficulty_color = difficulty_colors[
            level["difficulty"]
        ]

        difficulty_text = small_font.render(
            level["difficulty"],
            True,
            difficulty_color if is_unlocked else (100, 90, 115)
        )

        screen.blit(
            difficulty_text,
            difficulty_text.get_rect(
                center=(card.centerx, card.y + 125)
            )
        )

        #lock status
        if is_unlocked:
            status = "AVAILABLE"
            status_color = CYAN

        else:
            status = "LOCKED"
            status_color = (120, 105, 140)

        status_text = small_font.render(
            status,
            True,
            status_color
        )

        screen.blit(
            status_text,
            status_text.get_rect(
                center=(card.centerx, card.y + 160)
            )
        )

    #back button
    draw_button(
        level_back_button,
        "BACK",
        mouse_pos
    )

#footer
footer = small_font.render(
    "Complete a level to unlock the next one!",
    True,
    WHITE
)

screen.blit(
    footer,
    footer.get_rect(
        center=(WIDTH // 2, 425)
    )
)  

def draw_level_complete_screen():
    screen.fill(BACKGROUND)
    draw_menu_atmosphere()

    #dark overlay
    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    # title
    title = title_font.render(
        "LEVEL COMPLETE!",
        True,
        GOLD
    )

    screen.blit(
        title,
        title.get_rect(
            center=(WIDTH // 2, 105)
        )
    )

    # level name
    level_name = levels[selected_level]["name"]

    name_text = button_font.render(
        level_name,  
        True,
        PINK
    )
    screen.blit(
        name_text,
        name_text.get_rect(
            center=(WIDTH // 2, 175)
        )
    )

    # completion message
    message = small_font.render(
        "You made it through the challenge!",
        True,
        WHITE
    )

    screen.blit(
        message,
        message.get_rect(
            center=(WIDTH // 2, 220)
        )
    )

    #final score
    score_text = button_font.render(
        f"FINAL SCORE: {score}",
        True, CYAN
    )

    screen.blit(
        score_text,
        score_text.get_rect(
            center=(WIDTH // 2, 275)
        )
    )

    #coins collected
    coins_text = small_font.render(
        f"COINS COLLECTED: {coins_collected}",
        True,
        GOLD
    )

    screen.blit(
        coins_text,
        coins_text.get_rect(
            center=(WIDTH // 2, 315)
        )
    )

    # button
    draw_button(
        level_complete_button,
        "LEVEL SELECT",
        pygame.mouse.get_pos()
    )

# DRAW GROUND TEXTURES

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

# DRAW MUSHROOMS

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
# CREATE ENVIRONMENT
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

# UPDATE ENVIRONMENT
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

# DRAW ENVIRONMENT
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
# SPAWN PLATFORMS
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
# SPAWN GROUND GAPS

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

# draw coins
def draw_coins(coin, time):

    pulse = 1 + math.sin(time * 0.006) * 0.12

    coin_width = int(COIN_SIZE * pulse)

    coin_rect = pygame.Rect(
        coin.centerx - coin_width // 2,
        coin.centery - COIN_SIZE // 2,
        coin_width,
        COIN_SIZE
    )

    glow_surface = pygame.Surface(
        (COIN_SIZE + 24, COIN_SIZE + 24),
        pygame.SRCALPHA
    )

    pygame.draw.circle(
        glow_surface,
        (255, 200, 50, 45),
        (
            (COIN_SIZE + 24) // 2,
            (COIN_SIZE + 24) // 2
        ),
        COIN_SIZE // 2 + 10
    )

    screen.blit(
        glow_surface,
        (coin.centerx - (COIN_SIZE + 24) // 2,
         coin.centery - (COIN_SIZE + 24) // 2)
    )

    pygame.draw.ellipse(
        screen,
        GOLD,
        coin_rect
    )

    pygame.draw.ellipse(
        screen,
        LIGHT_GOLD,
        (
            coin_rect.x + 5,
            coin_rect.y + 3,
            max(4, coin_width - 10),
            COIN_SIZE - 6
        )
    )

    pygame.draw.circle(
        screen,
        GOLD,
        coin_rect.center,
        4
    )

# SPAWN OBSTACLES
def spawn_obstacle(x):

    if selected_level == 1:
        weights = [6, 2, 0, 3, 0, 0]

    elif selected_level == 2:
        weights = [3, 4, 1, 3, 2, 1]

    else:
        weights = [2, 4, 3, 2, 3, 2]

    obstacle_type = random.choices(
        [
            "spike",
            "double_spike",
            "triple_spike",
            "block",
            "moving_block",
            "hanging_spike"
        ],
        weights=weights,
        k=1
    )[0]

    if obstacle_type == "double_spike":
        spike_count = 2

    elif obstacle_type == "triple_spike":
        spike_count = 3
    else:
        spike_count = 1

    if obstacle_type == "block":
        obstacle_width = 40
    elif obstacle_type in ["moving_block", "hanging_spike"]:
        obstacle_width = 45
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
        if (
            x < saw["x"] + saw["radius"] + OBSTACLE_SAFE_DISTANCE
            and x + obstacle_width > saw["x"] - saw["radius"] - OBSTACLE_SAFE_DISTANCE
        ):
            return

    if obstacle_type in [
        "spike",
        "double_spike",
        "triple_spike"
    ]:
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

    elif obstacle_type == "moving_block":
        rect = pygame.Rect(
            x,
            GROUND_Y - 100,
            45,
            45
        )

        obstacle.append({
            "rect": rect,
            "type": "moving_block",
            "base_y": GROUND_Y - 100,
            "phase": random.uniform(0, 6.28),
            "amplitude": random.randint(35, 65)

        })

    elif obstacle_type == "hanging_spike":
        rect = pygame.Rect(
            x,
            250,
            45,
            70
        )

        obstacles.append({
            "rect": rect,
            "type": "hanging_spike"
        })

def spawn_saw(x):

    if selected_level == 1:
        return

    elif selected_level == 2:
        if random.random() > 0.35:
            return

    else:
        if random.random() > 0.60:
            return
    for gap in gaps:
        if (
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
    

# RESET GAME
def reset_game():


    global game_tutorial_active, game_tutorial_step
    global tutorial_orb_used, tutorial_pad_used
    global tutorial_gem_collected, tutorial_rose_collected
    global tutorial_finished
    global player, player_y, player_velocity
    global run_start_ticks
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
    global next_coin_x
    global coins_collected

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

    run_start_ticks = None

    game_tutorial_active = False
    game_tutorial_step = 0

    tutorial_orb_used = False
    tutorial_pad_used = False
    tutorial_gem_collected = False
    tutorial_rose_collected = False
    tutorial_finished = False

    combo = 0
    combo_timer = 0
    combo_bonus = 0


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
    coins.clear()
    coins_collected = 0

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
    next_coin_x = WIDTH + 500

    # Initialize grass, fireflies, and particles
    create_environment()

reset_game()

# MAIN GAME LOOP
while running:

    clock.tick(60)

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            continue

        if event.type == pygame.MOUSEWHEEL:

            if game_state == STATISTICS:

                stats_scroll -= event.y * stats_scroll_speed

                stats_scroll = max(
                    0,
                    min(stats_scroll, stats_scroll_limit)
                )

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mouse_pos = event.pos

                if pause_menu_active:

                    if resume_button.collidepoint(mouse_pos):

                        pause_menu_active = False

                        if pause_started_ticks is not None:

                            paused_duration = (
                                pygame.time.get_ticks() - pause_started_ticks
                            )

                            if run_start_ticks is not None:
                                run_start_ticks += paused_duration

                        if(
                            game_tutorial_active
                            and game_tutorial_step == 5
                            and tutorial_pause_opened
                        ):
                            tutorial_pause_resumed = True

                    elif restart_button.collidepoint(mouse_pos):
                        pause_menu_active = False
                        reset_game()
                        game_state = PLAYING


                    elif pause_menu_button.collidepoint(mouse_pos):
                        pause_menu_active = False
                        game_tutorial_active = False
                        show_achievements = False
                        game_state = MENU

                    elif pause_quit_button.collidepoint(mouse_pos):
                        save_data()
                        running = False

                    continue

                if game_tutorial_active:

                    if game_tutorial_step == 5 and pause_button.collidepoint(mouse_pos):
                        tutorial_pause_opened = True
                        pause_menu_active = True
                        pause_started_ticks = pygame.time.get_ticks()
                        continue

                    if game_tutorial_skip_button.collidepoint(mouse_pos):

                        game_tutorial_active = False
                        game_tutorial_completed = True
                        game_state = MENU
                        save_data()

                    elif tutorial_finished:

                        game_tutorial_active = False
                        game_tutorial_completed = True
                        game_state = MENU
                        save_data()

                    else:
                        if game_tutorial_step == 3 and not on_ground:

                            for orb in jump_orbs:
                                orb_area = orb["rect"].inflate(24, 24)

                                if player.colliderect(orb_area):
                                    player_velocity = -19
                                    on_ground = False
                                    tutorial_orb_used = True
                                    break

                        if game_tutorial_step == 5:
                            if pause_button.collidepoint(mouse_pos):
                                tutorial_pause_opened = True
                                pause_menu_active = True
                                pause_started_ticks = pygame.time.get_ticks()

                                continue

                        if on_ground:
                            player_velocity = JUMP_STRENGTH
                            on_ground = False
                    continue

                if tutorial_active:

                    if skip_tutorial_button.collidepoint(mouse_pos):

                        tutorial_active = False
                        tutorial_completed = True
                        save_data()

                    elif tutorial_targets[tutorial_step].collidepoint(mouse_pos):

                        tutorial_step += 1

                        if tutorial_step >= len(tutorial_targets):

                            tutorial_active = False
                            tutorial_completed = True
                            save_data()

                    

                    continue

                if(
                    game_state == PLAYING
                    and not game_over
                    and not pause_menu_active
                    and pause_button.collidepoint(mouse_pos)
                ):
                    pause_menu_active = True
                    continue

                click_effect_pos = mouse_pos
                click_effect_time = pygame.time.get_ticks()

                if game_state == WELCOME:

                    if continue_button.collidepoint(mouse_pos):

                        entered_name = name_input_text.strip()

                        if entered_name:

                            player_name = entered_name
                            game_state = MENU

                            if not tutorial_completed:
                                tutorial_active = True
                                tutorial_step = 0
                            save_data()

                elif game_state == MENU:

                    if stats_button.collidepoint(mouse_pos):
                        stats_scroll = 0
                        game_state = STATISTICS

                    elif play_button.collidepoint(mouse_pos):

                        show_achievements = False
                        game_state = LEVEL_SELECT

                    elif help_button.collidepoint(mouse_pos):
                        game_state = HOW_TO_PLAY

                    elif achievements_button.collidepoint(mouse_pos):
                        show_achievements = True
                        game_state = PLAYING

                    elif shop_button.collidepoint(mouse_pos):
                        game_state = SHOP

                    elif quit_button.collidepoint(mouse_pos):
                        save_data()
                        running = False

                elif game_state == LEVEL_SELECT:
                    if level_back_button.collidepoint(mouse_pos):
                        game_state = MENU

                    else:
                        for index, level_number in enumerate(levels):
                            if level_buttons[index].collidepoint(mouse_pos):
                                if level_number in unlocked_levels:
                                    selected_level = level_number
                                    game_state = PLAYING

                                    if not game_tutorial_completed:
                                        start_game_tutorial()

                                    else:
                                        reset_game()
                                        game_speed = levels[selected_level]["speed"]
                                break

                elif game_state == LEVEL_COMPLETE:

                    if level_complete_button.collidepoint(mouse_pos):
                        game_state = LEVEL_SELECT


                elif game_state == SHOP:
                    if cube_category_button.collidepoint(mouse_pos):
                        shop_category = "CUBES"
                        selected_shop_item = None

                    elif trail_category_button.collidepoint(mouse_pos):
                        shop_category = "TRAILS"
                        selected_shop_item = None

                    elif death_category_button.collidepoint(mouse_pos):
                        shop_category = "DEATH EFFECTS"
                        selected_shop_item = None

                    elif back_button.collidepoint(mouse_pos):
                        game_state = MENU
                        selected_shop_item = None

                    else:
                        item_selected = False

                        for index, item_button in enumerate(shop_item_buttons):

                            if item_button.collidepoint(mouse_pos):

                                item = shop_items[shop_category][index]
                                item_name = item["name"]
                                item_price = item["price"]

                                selected_shop_item = item_name
                                item_selected = True

                                if item_name in owned_items:

                                    equip_shop_item(item_name, shop_category)

                                    shop_notice = "Item equipped!"
                                    shop_notice_time = pygame.time.get_ticks()

                                elif coin_balance >= item_price:

                                    coin_balance -= item_price
                                    owned_items.append(item_name)

                                    equip_shop_item(item_name, shop_category)

                                    shop_notice = "Purchased and equipped!"
                                    shop_notice_time = pygame.time.get_ticks()

                                else:
                                    shop_notice = "Not enough coins!"
                                    shop_notice_time = pygame.time.get_ticks()

                                break
                        if not item_selected:
                            for index, item in enumerate(shop_items[shop_category]):
                                item_card = pygame.Rect(
                                    105 + index * 240,
                                    240,
                                    210,
                                    145
                                )

                                if item_card.collidepoint(mouse_pos):
                                    selected_shop_item = item["name"]
                                    break

                elif game_state == HOW_TO_PLAY:

                    if back_button.collidepoint(mouse_pos):
                        game_state = MENU

                    elif game_tutorial_replay_button.collidepoint(mouse_pos):
                        game_state = PLAYING
                        start_game_tutorial()

                elif game_state == STATISTICS:

                    if back_button.collidepoint(mouse_pos):

                        editing_name = False
                        stats_scroll = 0
                        game_state = MENU

                    elif reset_data_button.collidepoint(mouse_pos):

                        editing_name = False
                        game_state = CONFIRM_RESET

                    elif (
                        not editing_name
                        and edit_name_button.move(0, -stats_scroll).collidepoint(mouse_pos)
                    ):
                        editing_name = True
                        name_input_text = player_name

                    elif (
                        editing_name
                        and save_name_button.move(0, -stats_scroll).collidepoint(mouse_pos)
                    ):

                        entered_name = name_input_text.strip()

                        if entered_name:

                            player_name = entered_name
                            save_data()
                            editing_name = False

                elif game_state == CONFIRM_RESET:

                    if confirm_reset_button.collidepoint(mouse_pos):

                        reset_saved_data()
                        stats_scroll = 0
                        editing_name = False
                        game_state = WELCOME

                    elif cancel_reset_button.collidepoint(mouse_pos):

                        game_state = STATISTICS

                elif game_state == PLAYING:

                    if show_achievements:

                        if back_button.collidepoint(mouse_pos):
                            show_achievements = False
                            game_state = MENU

                    elif game_over:

                        if back_button.collidepoint(mouse_pos):
                            reset_game()
                            show_achievements = False
                            game_state = MENU

                    else:
                        touching_orb = False

                        for orb in jump_orbs:
                            orb_area = orb["rect"].inflate(24, 24)

                            if player.colliderect(orb_area) and not on_ground:
                                touching_orb = True
                                break

                        if touching_orb and not on_ground:
                            player_velocity = -19
                            on_ground = False

                            total_orb_activations += 1
                            save_data()

                            if total_orb_activations >= 5:
                                unlock_achievement("first_flight")

                        elif on_ground:
                            target_scale_x = 0.85
                            target_scale_y = 1.2
                            player_animation_timer = 8
                            player_velocity = JUMP_STRENGTH
                            on_ground = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                
                if game_state == PLAYING and not game_over and not show_achievements:

                    if not pause_menu_active:

                        pause_menu_active = True
                        pause_started_ticks = pygame.time.get_ticks()

                        if game_tutorial_active and game_tutorial_step == 5:
                            tutorial_pause_opened = True
                    else:
                        pause_menu_active = False

                        if pause_started_ticks is not None:
                            paused_duration = (
                                pygame.time.get_ticks() - pause_started_ticks
                            )

                            if run_start_ticks is not None:
                                run_start_ticks += paused_duration

                        if(
                            game_tutorial_active
                            and game_tutorial_step == 5
                            and tutorial_pause_opened
                        ):
                            tutorial_pause_resumed = True

                continue

            if game_state == WELCOME:

                if event.key == pygame.K_BACKSPACE:
                    name_input_text = name_input_text[:-1]

                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    entered_name = name_input_text.strip()

                    if entered_name:
                        player_name = entered_name
                        game_state = MENU

                        if not tutorial_completed:
                            tutorial_active = True
                            tutorial_step = 0

                        save_data()

                elif event.unicode.isprintable() and len(name_input_text) < 16:
                    name_input_text += event.unicode

            #stats name editing
            elif game_state == STATISTICS and editing_name:

                if event.key == pygame.K_BACKSPACE:
                    name_input_text = name_input_text[:-1]

                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    entered_name = name_input_text.strip()

                    if entered_name:
                        player_name = entered_name
                        save_data()
                        editing_name = False

                elif event.unicode.isprintable() and len(name_input_text) < 16:
                    name_input_text += event.unicode

            elif event.key == pygame.K_SPACE and game_state == PLAYING:

                if game_over:
                    reset_game()
                    game_state = PLAYING

                elif show_achievements:
                    pass

                elif game_tutorial_active:

                    if game_tutorial_step == 3 and not on_ground:
                        for orb in jump_orbs:
                            orb_area = orb["rect"].inflate(24, 24)

                            if player.colliderect(orb_area):
                                player_velocity = -19
                                on_ground = False
                                tutorial_orb_used = True
                                break

                    if on_ground:
                        player_velocity = JUMP_STRENGTH
                        on_ground = False
                else:
                    touching_orb = False

                    for orb in jump_orbs:
                        orb_area = orb["rect"].inflate(24, 24)

                        if player.colliderect(orb_area) and not on_ground:
                            touching_orb = True
                            break

                    if touching_orb:
                        player_velocity = -19
                        on_ground = False

                        total_orb_activations += 1
                        save_data()

                        if total_orb_activations >= 5:
                            unlock_achievement("first_flight")

                    elif on_ground:
                        target_scale_x = 0.85
                        target_scale_y = 1.2
                        player_animation_timer = 8
                        player_velocity = JUMP_STRENGTH
                        on_ground = False

    # UPDATE GAME
    if(
        game_state == PLAYING
        and not game_over
        and not show_achievements
        and not game_tutorial_active
        and not pause_menu_active
    ):
        if run_start_ticks is None:
            run_start_ticks = pygame.time.get_ticks()

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

        for coin in coins:
            coin.x -= game_speed

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

        coins[:] = [coin for coin in coins if coin.right > 0]

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

        #generate coins 

        next_coin_x -= game_speed

        if next_coin_x < WIDTH:

            near_gap = any(
                gap.left - 80 <= WIDTH <= gap.right + 80
                for gap in gaps
            )

            near_obstacle = any(
                abs(obstacle["rect"].centerx - WIDTH) < 120
                for obstacle in obstacles
            )

            if not near_gap and not near_obstacle:

                coin_y = random.randint(300, 365)

                coins.append(
                    pygame.Rect(WIDTH, coin_y, COIN_SIZE, COIN_SIZE)
                )

            next_coin_x = WIDTH + random.randint(600, 900)


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

        # Generate Trail
        if (
            game_state == PLAYING
            and not game_over
            and not pause_menu_active
        ):
            trail_timer += 1

            if trail_timer >= TRAIL_SPAWN_DELAY:

                create_trail_particle()
                trail_timer = 0

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
                total_roses += 1

                save_data()

                if total_roses >= 20:
                    unlock_achievement("rose_keeper")
        
        for gem in gems[:]:

            if player.colliderect(gem):

                gems.remove(gem)

                gem_count += 1
                total_gems += 1

                score += 25
                save_data()

                if total_gems >= 1:
                    unlock_achievement("first_bloom")

                if total_gems >= 10:
                    unlock_achievement("gem_collector")

                if total_gems >= 50:
                    unlock_achievement("gem_hoarder")

                # increase combo
                combo += 1
                combo_timer = COMBO_DURATION

                if combo > best_combo:
                    best_combo = combo
                    save_data()

                if best_combo >= 10:
                    unlock_achievement("combo_master")

                if combo >= 5:
                    unlock_achievement("combo_starter")


                # calculate combo bonus
                combo_bonus = combo * 10
                score += combo_bonus
        #collect coims
        for coin in coins[:]:
            if player.colliderect(coin):

                coins.remove(coin)

                coin_balance += 1
                coins_collected += 1

                save_data()
        # Score and speed
        score += 1

        if score >= 1000:
            unlock_achievement("high_scorer")

        if score > high_score:

            high_score = score
            save_data()

        game_speed = min(
            10,
            5 + score // 1000
        )

    #check level completion
    if (
        game_state == PLAYING
        and score >= levels[selected_level]["target_score"]
    ):
        complete_level()

    # update gameplay tut
    if game_tutorial_active and not pause_menu_active:

        ground_texture_offset += game_speed
        update_environment()

        for i in range(len(mushrooms)):
            x, y, size = mushrooms[i]
            mushrooms[i] = (x - game_speed, y, size)

        mushrooms[:] = [
            mushroom for mushroom in mushrooms
            if mushroom[0] > -50
        ]

        if game_tutorial_step == 0:
            for obstacle in obstacles:
                obstacle["rect"].x -= game_speed

        if game_tutorial_step <= 1:
            for gem in gems:
                gem.x -= game_speed

                if gem.right < 0:
                    gem.x = WIDTH + random.randint(300, 450)
                    gem.y = random.randint(300, 365)

        if game_tutorial_step <= 2:
            for rose in roses:
                rose.x -= game_speed

                if rose.right < 0:
                    rose.x = WIDTH + random.randint(300, 450)
                    rose.y = GROUND_Y - 35

        if game_tutorial_step <= 3:
            for orb in jump_orbs:
                orb["rect"].x -= game_speed
                orb["pulse"] += 0.08

                if orb["rect"].right < 0:
                    orb["rect"].x = WIDTH + random.randint(300, 450)

        if game_tutorial_step <= 4:
            for pad in jump_pads:
                pad.x -= game_speed

                if pad.right < 0:
                    pad.x = WIDTH + random.randint(350, 500)

        previous_bottom = player.bottom

        player_velocity += GRAVITY
        player_y += player_velocity
        player.y = int(player_y)

        on_ground = False

        if player_velocity >= 0 and player.bottom >= GROUND_Y:
            player.bottom = GROUND_Y
            player_y = float(player.y)
            player_velocity = 0
            on_ground = True

        if game_tutorial_step == 0:
            for obstacle in obstacles:
                if player.colliderect(obstacle["rect"]):
                    player.bottom = GROUND_Y
                    player_y = float(player.y)
                    player_velocity = 0
                    on_ground = True

                    obstacle["rect"].x = WIDTH + random.randint(300, 450)

            if obstacles and obstacles[0]["rect"].right < player.left:
                obstacles.clear()
                game_tutorial_step = 1

        elif game_tutorial_step == 1:
            for gem in gems[:]:
                if player.colliderect(gem):
                    gems.remove(gem)
                    tutorial_gem_collected = True

            if tutorial_gem_collected:
                game_tutorial_step = 2

        elif game_tutorial_step == 2:
            for rose in roses[:]:
                if player.colliderect(rose):
                    roses.remove(rose)
                    tutorial_rose_collected = True

            if tutorial_rose_collected:
                    game_tutorial_step = 3

        elif game_tutorial_step == 3:
            if tutorial_orb_used:
                jump_orbs.clear()
                game_tutorial_step = 4

        elif game_tutorial_step == 4:
            for pad in jump_pads:
                horizontal_overlap = (
                    player.right > pad.left
                    and player.left < pad.right
                )               
                crossed_pad_top = (
                    previous_bottom <= pad.top
                    and player.bottom >= pad.top
                )

                if(
                    horizontal_overlap
                    and crossed_pad_top
                    and player_velocity >= 0

                ):

                    player.bottom = pad.top
                    player_y = float(player.y)
                    player_velocity = -19
                    on_ground = False
                    tutorial_pad_used = True

            if tutorial_pad_used:
                jump_pads.clear()
                game_tutorial_step = 5

        elif game_tutorial_step == 5:
            if tutorial_pause_resumed:
                game_tutorial_step = 6

        elif game_tutorial_step == 6:
            tutorial_finished = True

        if player.bottom >= GROUND_Y and player_velocity >= 0:
            player.bottom = GROUND_Y
            player_y = float(player.y)
            player_velocity = 0
            on_ground = True
        
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

    # update trail particles
    for particle in trail_particles[:]:

        particle["x"] -= game_speed
        particle["life"] -= 1
        particle["radius"] *= 0.96

        if particle["life"] <= 0 or particle["radius"] < 1:
            trail_particles.remove(particle)


    # update death particles

    if game_over and not death_effect_started:

        create_death_effect()
        death_effect_started = True

        runs_completed += 1

        if run_start_ticks is not None:
            survival_time = (
                pygame.time.get_ticks() - run_start_ticks
            ) // 1000

            if survival_time > best_survival_time:
                best_survival_time = survival_time

        save_data()

        if runs_completed >= 20:
            unlock_achievement("dedicated_player")

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

    # DRAW BACKGROUND

    draw_background()

    # DRAW NORMAL GROUND
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
    # DRAW GROUND GAP EDGES
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

    # DRAW GRASS, FIREFLIES, AND PARTICLES

    draw_environment()

    # DRAW ELEVATED PLATFORMS

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

    # DRAW OBSTACLES

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

    # DRAW ROSES
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

    current_time = pygame.time.get_ticks()

    for coin in coins:
        draw_coins(coin, current_time)

    
    # DRAW MUSHROOMS

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

    # draw trail
    for particle in trail_particles:
        pygame.draw.circle(
            screen,
            particle["color"],
            (int(particle["x"]), int(particle["y"])),
            max(1, int(particle["radius"]))
        )

    # DRAW PLAYER
    # create animation

    animated_width = int(PLAYER_WIDTH * player_scale_x)
    animated_height = int(PLAYER_HEIGHT * player_scale_y)

    animated_width = max(1, animated_width)
    animated_height = max(1, animated_height)

    cube_surface = pygame.Surface(
        (animated_width, animated_height),
        pygame.SRCALPHA
    )

    # select cube skin
    if equipped_cube == "Rose Cube":
        cube_color = ROSE_CUBE_MAIN
        outline_color = ROSE_CUBE_OUTLINE

    elif equipped_cube == "Neon Cube":
        cube_color = NEON_CUBE_MAIN
        outline_color = NEON_CUBE_OUTLINE

    else:
        cube_color = NEON_PURPLE
        outline_color = NEON_CYAN

    #MAIN CUBE
    pygame.draw.rect(
        cube_surface,
        cube_color,
        (0, 0, animated_width, animated_height),
        border_radius=5
    )

    #outline
    pygame.draw.rect(
        cube_surface,
        outline_color,
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

    # TITLE AND SCORE
    if game_state == PLAYING and not show_achievements:

        title = hud_title_font.render(
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

        #coin hud

        coin_text = small_font.render(
            f"Coins: {coin_balance}",
            True,
            GOLD
        )

        screen.blit(coin_text, (25, 170))

    # ACHIEVEMENT NOTIFICATION

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
    # ACHIEVEMENT COLLECTION
    if show_achievements:

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(210)
        overlay.fill((10, 5, 30))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(50, 35, 800, 430)

        pygame.draw.rect(
            screen, DARK_PURPLE, panel, border_radius=18
        )

        pygame.draw.rect(
            screen, CYAN, panel, 3, border_radius=18
        )

        heading_font = pygame.font.SysFont(
            "bahnschrift", 38, bold=True
        )

        heading = heading_font.render(
            "ACHIEVEMENTS", True, PINK
        )

        screen.blit(
            heading,
            heading.get_rect(
                center=(WIDTH // 2, 75)
            )
        )

        progress_values = {
            "first_bloom": f"{min(total_gems, 1)}/1 gem",
            "gem_collector": f"{min(total_gems, 10)}/10 gems",
            "combo_starter": f"{min(best_combo, 5)}/5 combo",
            "high_scorer": f"{min(high_score, 1000)}/1000 points",
            "gem_hoarder": f"{min(total_gems, 50)}/50 gems",
            "rose_keeper": f"{min(total_roses, 20)}/20 roses",
            "combo_master": f"{min(best_combo, 10)}/10 combo",
            "first_flight": f"{min(total_orb_activations, 5)}/5 activations",
            "dedicated_player": f"{min(runs_completed, 20)}/20 runs"
        } 

        progress_amounts = {
            "first_bloom": min(total_gems / 1, 1),
            "gem_collector": min(total_gems / 10, 1),
            "combo_starter": min(best_combo / 5, 1),
            "high_scorer": min(high_score / 1000, 1),
            "gem_hoarder": min(total_gems / 50, 1),
            "rose_keeper": min(total_roses / 20, 1),
            "combo_master": min(best_combo / 10, 1),
            "first_flight": min(total_orb_activations / 5, 1),
            "dedicated_player": min(runs_completed / 20, 1)
        }

        name_font = pygame.font.SysFont(
            "bahnschrift", 17, bold=True
        )

        desc_font = pygame.font.SysFont(
            "bahnschrift", 13
        )

        status_font = pygame.font.SysFont(
            "bahnschrift", 11, bold=True
        )

        progress_font = pygame.font.SysFont(
            "bahnschrift", 12
        )

        card_width = 245
        card_height = 86

        start_x = 70
        start_y = 112

        horizontal_spacing = 255
        vertical_spacing = 96

        for i, (achievement_id, achievement) in enumerate(
            achievements.items()
        ):

            column = i % 3
            row = i // 3

            card_x = start_x + column * horizontal_spacing
            card_y = start_y + row * vertical_spacing

            card = pygame.Rect(
                card_x,
                card_y,
                card_width,
                card_height
            )

            unlocked = achievement["unlocked"]

            card_color = (
                (65, 40, 105) if unlocked
                else (35, 22, 65)
            )

            border_color = (
                CYAN if unlocked
                else (100, 65, 130)
            )

            pygame.draw.rect(
                screen,
                card_color,
                card,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                border_color,
                card,
                2,
                border_radius=10
            )

            name_text = name_font.render(
                achievement["name"],
                True,
                PINK if unlocked else WHITE
            )

            screen.blit(
                name_text,
                (card_x + 10, card_y + 7)
            )

            status_text = status_font.render(
                "UNLOCKED" if unlocked else "LOCKED",
                True,
                CYAN if unlocked else(170, 150, 190)
            )

            screen.blit(
                status_text,
                (card.right - status_text.get_width() - 10, card_y + 11)
            )

            desc_text = desc_font.render(
                achievement["description"],
                True,
                WHITE
            )

            screen.blit(
                desc_text,
                (card_x + 10, card_y + 31)
            )

            progress_text = progress_font.render(
                progress_values[achievement_id],
                True,
                CYAN
            )

            screen.blit(
                progress_text,
                (card_x + 10, card_y + 52)
            )

            bar_rect = pygame.Rect(
                card_x + 10,
                card_y + 72,
                card_width - 20,
                6
            )

            pygame.draw.rect(
                screen,
                (20, 12, 40),
                bar_rect,
                border_radius=4
            )

            fill_width = int(
                bar_rect.width * progress_amounts[achievement_id]
            )

            if fill_width > 0:

                pygame.draw.rect(
                    screen,
                    CYAN if unlocked else NEON_PURPLE,
                    (
                        bar_rect.x,
                        bar_rect.y,
                        fill_width,
                        bar_rect.height
                    ),
                    border_radius=4
                )
        mouse_pos = pygame.mouse.get_pos()
        draw_button(back_button, "BACK", mouse_pos)

    # GAME OVER
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
            "Click below to return",
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

        mouse_pos = pygame.mouse.get_pos()

        draw_button(back_button, "BACK TO MENU", mouse_pos)

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

        if not isinstance(particle["color"], (tuple, list)):
            print("INVALID DEATH PARTICLE COLOR:", particle["color"])
            continue

        if particle.get("shape") == "star":

            draw_star(
                particle_surface,
                (*particle["color"], alpha),
                center,
                size * 2
            )

        else:

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

    # MAIN MENU

    if game_state == MENU:

        menu_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )
        menu_overlay.fill((35, 12, 65, 100))
        screen.blit(menu_overlay, (0, 0))

        draw_menu_atmosphere()

        #Game title
        title = title_font.render(
            "ROSAS RUSH",
            True,
            PINK
        )
        screen.blit(
           title,
            title.get_rect(
                center=(WIDTH // 2,95)
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
                center=(WIDTH // 2, 155)
            )
        )

        #menu options
        mouse_pos = pygame.mouse.get_pos()

        draw_stats_icon(stats_button, mouse_pos)

        draw_button(play_button, "PLAY", mouse_pos)
        draw_button(help_button, "HOW TO PLAY", mouse_pos)
        draw_button(achievements_button, "ACHIEVEMENTS", mouse_pos)
        draw_button(shop_button, "COIN SHOP", mouse_pos)
        draw_button(quit_button, "QUIT", mouse_pos) 

        coin_text = small_font.render(
            str(coin_balance),
            True,
            GOLD
        )

        screen.blit(coin_text, (WIDTH - 105, 30))

        pygame.draw.circle(
            screen,
            GOLD,
            (WIDTH - 120, 45),
            10
        )

        pygame.draw.circle(
            screen,
            LIGHT_GOLD,
            (WIDTH - 120, 45),
            5
        )

    elif game_state == LEVEL_SELECT:
        draw_level_select_screen()

    elif game_state == LEVEL_COMPLETE:
        draw_level_complete_screen()

    elif game_state == SHOP:

        screen.fill(BACKGROUND)
        draw_menu_atmosphere()

        shop_title = title_font.render(
            "COIN SHOP",
            True,
            GOLD
        )

        screen.blit(
            shop_title,
            shop_title.get_rect(center=(WIDTH // 2, 65))
        )

        coin_text = small_font.render(
            f"COINS: {coin_balance}",
            True,
            GOLD
        )

        screen.blit(coin_text, (WIDTH - 170, 25))

        shop_panel = pygame.Rect(80, 115, 740, 275)

        pygame.draw.rect(
            screen,
            DARK_PURPLE,
            shop_panel,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            PURPLE,
            shop_panel,
            3,
            border_radius=18
        )

        shop_message = small_font.render(
            "Choose a category to customize your cube!",
            True,
            WHITE
        )

        screen.blit(
            shop_message,
            shop_message.get_rect(center=(WIDTH // 2, 155))
        )

        draw_button(
            cube_category_button,
            "CUBES",
            pygame.mouse.get_pos()
        )

        draw_button(
            trail_category_button,
            "TRAILS",
            pygame.mouse.get_pos()
        )

        draw_button(
            death_category_button,
            "DEATH EFFECTS",
            pygame.mouse.get_pos()
        )

        current_items = shop_items[shop_category]

        for index, item in enumerate(current_items):
            item_card = pygame.Rect(
                105 + index * 240,
                240,
                210,
                145
            )

            # item card hover animation
            mouse_over_card = item_card.collidepoint(mouse_pos)

            card_color = (45, 28, 90) if mouse_over_card else (35, 20, 75)
            border_color = CYAN if mouse_over_card else PURPLE
            border_width = 3 if mouse_over_card else 2

            pygame.draw.rect(
                screen,
                card_color,
                item_card,
                border_radius=12
            )

            pygame.draw.rect(
                screen,
                border_color,
                item_card,
                border_width,
                border_radius=12
            )

            item_name_text = small_font.render(
                item["name"],
                True,
                WHITE
            )

            screen.blit(
                item_name_text,
                item_name_text.get_rect(
                    center=(item_card.centerx, 260)
                )
            )

            # item prev

            preview_x = item_card.centerx
            preview_y = 305

            if shop_category == "CUBES":

                if item["name"] == "Rose Cube":
                    preview_color = ROSE_CUBE_MAIN
                    preview_outline = ROSE_CUBE_OUTLINE

                elif item["name"] == "Neon Cube":
                    preview_color = NEON_CUBE_MAIN
                    preview_outline = NEON_CUBE_OUTLINE

                else:
                    preview_color = NEON_PURPLE
                    preview_outline = NEON_CYAN

                preview_surface = pygame.Surface(
                    (40, 40),
                    pygame.SRCALPHA
                )

                pygame.draw.rect(
                    preview_surface,
                    preview_color,
                    (4, 4, 32, 32),
                    border_radius=5
                )

                pygame.draw.rect(
                    preview_surface,
                    preview_outline,
                    (4, 4, 32, 32),
                    3,
                    border_radius=5
                )

                pygame.draw.rect(
                    preview_surface,
                    PINK,
                    (12, 12, 16, 16),
                    2,
                    border_radius=3
                )

                if item["name"] == "Neon Cube":
                    glow_pulse =(
                        math.sin(pygame.time.get_ticks() * 0.006) + 1
                    ) / 2

                    glow_alpha = int(40 + glow_pulse * 100)

                    glow_surface = pygame.Surface(
                        (65, 65),
                        pygame.SRCALPHA
                    )

                    pygame.draw.circle(
                        glow_surface,
                        (*CYAN, glow_alpha),
                        (32, 32),
                        25
                    )

                    screen.blit(
                        glow_surface,
                        glow_surface.get_rect(
                            center=(preview_x, preview_y)
                        )
                    )

                rotation_angle = (
                    pygame.time.get_ticks() * 0.08
                ) % 360

                rotated_preview = pygame.transform.rotate(
                    preview_surface,
                    rotation_angle
                )

                screen.blit(
                    rotated_preview,
                    rotated_preview.get_rect(
                        center=(preview_x, preview_y)
                    )
                )

            elif shop_category == "TRAILS":

                preview_time = pygame.time.get_ticks() * 0.005

                if item["name"] == "Pink Trail":
                    preview_colors = [PINK]

                elif item["name"] == "Cyan Trail":
                    preview_colors = [CYAN] * 3


                else:
                    preview_colors = RAINBOW_COLORS

                for particle_index in range(5):

                    particle_x = (
                        preview_x - 35 +
                        (particle_index * 17) -
                        (preview_time * 20) % 17
                    )

                    if item["name"] == "Rainbow Trail":
                        color = preview_colors[
                            (particle_index + int(preview_time)) %
                            len(preview_colors)
                        ]

                    else:
                        color = preview_colors[0]

                    particle_size = 7 - particle_index * 0.7

                    pygame.draw.circle(
                        screen,
                        color,
                        (
                            int(particle_x),
                            int(preview_y)
                        ),
                        max(2, int(particle_size))
                    )

            else:
                preview_time = pygame.time.get_ticks() * 0.004

                if item["name"] == "Rose Burst":
                    preview_colors = [PINK, ROSE_RED, PINK]

                elif item["name"] == "Star Burst":
                    preview_colors = [WHITE, GOLD, LIGHT_GOLD]

                else:
                    preview_colors = [CYAN, NEON_PURPLE, NEON_CYAN]

                for particle_index in range(8):

                    angle = (
                        particle_index * 45 +
                        preview_time * 30
                    )

                    distance = 12 + (
                        math.sin(preview_time + particle_index) * 8
                    )

                    particle_x = preview_x + math.cos(
                        math.radians(angle)
                    ) * distance

                    particle_y = preview_y + math.sin(
                        math.radians(angle)
                    ) * distance

                    color = preview_colors[
                        particle_index % len(preview_colors)
                    ]

                    particle_size = 4 + int(
                        (math.sin(preview_time * 2 + particle_index) + 1) * 2
                    )

                    if item["name"] == "Star Burst":
                        draw_star(
                            screen,
                            color,
                            (int(particle_x), int(particle_y)),
                            particle_size + 3
                        )

                    else:
                        pygame.draw.circle(
                            screen,
                            color,
                            (int(particle_x), int(particle_y)),
                            particle_size
                        )

            if shop_category == "CUBES":
                equipped_item = equipped_cube

            elif shop_category == "TRAILS":
                equipped_item = equipped_trail

            else:
                equipped_item = equipped_death_effect

            if item["name"] == selected_shop_item:
                pygame.draw.rect(
                    screen,
                    GOLD,
                    item_card,
                    4,
                    border_radius=12
                )

            elif item["name"] == equipped_item:
                pygame.draw.rect(
                    screen,
                    CYAN,
                    item_card,
                    3,
                    border_radius=12
                )

            if item["name"] == equipped_item:
                button_label = "EQUIPPED"

            elif item["name"] in owned_items:
                button_label = "EQUIP"

            else:
                button_label = f"BUY - {item['price']}"

            draw_button(
                shop_item_buttons[index],
                button_label,
                pygame.mouse.get_pos()
            )

        if shop_notice:
            elapsed = pygame.time.get_ticks() - shop_notice_time

            if elapsed < 2500:
                notice_alpha = 255

                if elapsed > 1800:
                    notice_alpha = int(
                        255 * (2500 - elapsed) / 700
                    )

                notice_text = small_font.render(
                    shop_notice,
                    True,
                    GREEN if "Purchased" in shop_notice else CYAN
                )

                notice_text.set_alpha(notice_alpha)

                screen.blit(
                    notice_text,
                    notice_text.get_rect(
                        center=(WIDTH // 2, 374)
                    )
                )
            else:
                shop_notice = ""

            if selected_shop_item is not None:

                selected_item_data = next(
                    (
                        item for item in shop_items[shop_category]
                        if item["name"] == selected_shop_item
                    ),
                    None
                )
                if selected_item_data is not None:

                    inspection_panel = pygame.Rect(
                        190, 100, 520, 300
                    )

                    pygame.draw.rect(
                        screen,
                        (30, 18, 65),
                        inspection_panel,
                        border_radius=18
                    )

                    pygame.draw.rect(
                        screen,
                        GOLD,
                        inspection_panel,
                        3,
                        border_radius=18
                    )

                    inspection_title = title_font.render(
                        selected_item_data["name"],
                        True,
                        WHITE
                    )

                    screen.blit(
                        inspection_title,
                        inspection_title.get_rect(
                            center=(WIDTH // 2, 140)
                        )
                    )

                    price_text = small_font.render(
                        f"Price: {selected_item_data['price']} coins",
                        True,
                        GOLD
                    )

                    screen.blit(
                        price_text,
                        price_text.get_rect(
                            center=(WIDTH // 2, 185)
                        )
                    )

                    if selected_shop_item in owned_items:
                        status_message = "OWNED"
                        status_color = CYAN

                    else:
                        status_message = "NOT OWNED"
                        status_color = PINK

                    status_text = small_font.render(
                        status_message,
                        True,
                        status_color
                    )

                    screen.blit(
                        status_text,
                        status_text.get_rect(
                            center=(WIDTH // 2, 225)
                        )
                    )

        draw_button(back_button, "BACK", pygame.mouse.get_pos())


        #wc screen
    elif game_state == WELCOME:

        draw_menu_atmosphere()

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((15, 5, 35, 175))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(150, 55, 600, 390)

        pygame.draw.rect(
            screen,
            (40, 20, 75),
            panel,
            border_radius=22
        )

        pygame.draw.rect(
            screen,
            NEON_PURPLE,
            panel,
            3,
            border_radius=22
        )

        welcome_heading = welcome_title_font.render(
            "ROSAS RUSH",
            True,
            PINK
        )

        screen.blit(
            welcome_heading,
            welcome_heading.get_rect(
                center=(WIDTH // 2, 125)
            )
        )

        welcome_text = welcome_subtitle_font.render(
            "WELCOME, PLAYER!",
            True,
            WHITE
        )

        screen.blit(
            welcome_text,
            welcome_text.get_rect(
                center=(WIDTH // 2, 190)
            )
        )
        instruction = welcome_text_font.render(
            "What should we call you?",
            True,
            CYAN
        )

        screen.blit(
            instruction,
            instruction.get_rect(
                center=(WIDTH // 2, 225)
            )
        )

        pygame.draw.rect(
            screen,
            (25, 12, 55),
            welcome_input_box,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            CYAN,
            welcome_input_box,
            2, 
            border_radius=10
        )

        if name_input_text:

            name_text = welcome_input_font.render(
                name_input_text,
                True,
                WHITE

            )

        else:

            name_text = welcome_input_font.render(
                "Enter your player name...",
                True,
                (155, 140, 180)
            )

        screen.blit(
            name_text,
            (welcome_input_box.x + 15, welcome_input_box.y + 14)
        )

        mouse_pos = pygame.mouse.get_pos()

        draw_button(
            continue_button,
            "CONTINUE",
            mouse_pos
        )

        hint = pygame.font.SysFont(
            "bahnschrift", 16
        ).render(
            "Your name will be saved automatically.",
            True,
            (185, 165, 210)
        )

        screen.blit(
            hint,
            hint.get_rect(
                center=(WIDTH // 2, 405)
            )
        )
        # HOW TO PLAY SCREEN

    elif game_state == HOW_TO_PLAY:

        menu_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        menu_overlay.fill((25, 10, 55, 175))
        screen.blit(menu_overlay, (0, 0))

        heading = how_title_font.render(
            "HOW TO PLAY",
            True,
            PINK
        )

        screen.blit(
            heading,
            heading.get_rect(
                center=(WIDTH // 2, 75)
            )
        )

        subtitle = small_font.render(
            "LEARN THE BASICS BEFORE YOU RUSH",
            True,
            CYAN
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(
                center=(WIDTH // 2, 120)
            )
        )

        instructions = [
            ("PRESS SPACE", "Jump over obstacles"),
            ("CLICK ORB", "Activate jump orbs"),
            ("COLLECT", "Gather gems and roses"),
            ("AVOID", "Spikes, saws, and gaps"),
            ("TAP/CLICK", "Navigate the gems menus")
        ]

        card_x = 145
        card_width = 610
        card_height = 42
        start_y = 160
        spacing = 50

        for i, (control, description) in enumerate(instructions):

            card_y = start_y + i * spacing

            card = pygame.Rect(
                card_x,
                card_y,
                card_width,
                card_height
            )

            pygame.draw.rect(
                screen,
                (48, 25, 82),
                card,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                (100, 65, 150),
                card,
                width=1,
                border_radius=10
            )

            control_text = instruction_font.render(
                control,
                True,
                CYAN
            )

            screen.blit(
                control_text,
                (card_x + 25, card_y + 11)
            )

            description_text = small_font.render(
                description,
                True,
                WHITE
            )

            screen.blit(
                description_text,
                (card_x + 300, card_y + 10)
            )

        mouse_pos = pygame.mouse.get_pos()

        draw_button(back_button, "BACK", mouse_pos)

        draw_button(
            game_tutorial_replay_button,
            "PRACTICE TUTORIAL",
            mouse_pos
        )


# STAT PAGE

    elif game_state == STATISTICS:

        stats_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        stats_overlay.fill((25, 10, 55, 190))
        screen.blit(stats_overlay, (0,0))

        panel = pygame.Rect(50, 25, 800, 450)

        pygame.draw.rect(
            screen,
            (40, 20, 75),
            panel,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            PURPLE,
            panel,
            2,
            border_radius=20
        )

        stats_scroll_limit = max(
            0,
            stats_content_height - stats_viewport.height
        )

        stats_scroll = max(
            0,
            min(stats_scroll, stats_scroll_limit)
        )

        screen.set_clip(stats_viewport)

        heading = how_title_font.render(
            "YOUR STATISTICS",
            True, PINK
        )

        screen.blit(
            heading,
            heading.get_rect(
                center=(WIDTH // 2, 90 - stats_scroll)
            )
        )

        if not editing_name:

            name_display = small_font.render(
                f"PLAYER: {player_name}",
                True,
                CYAN
            )

            screen.blit(
                name_display,
                (
                    stats_name_box.x + 12,
                    stats_name_box.y + 7 - stats_scroll
                )
            )

            scrolled_edit_button = edit_name_button.copy()
            scrolled_edit_button.y -= stats_scroll

            mouse_pos = pygame.mouse.get_pos()

            draw_button(
                scrolled_edit_button,
                "EDIT NAME",
                mouse_pos
            )

        else:

            scrolled_name_box = stats_name_box.copy()
            scrolled_name_box.y -= stats_scroll

            pygame.draw.rect(
                screen,
                (25, 12, 55),
                scrolled_name_box,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                CYAN,
                scrolled_name_box,
                2,
                border_radius=8
            )

            edit_text = small_font.render(
                name_input_text,
                True,
                WHITE
            )

            screen.blit(
                edit_text,
                (stats_name_box.x + 12, stats_name_box.y + 7 - stats_scroll)
            )

            mouse_pos = pygame.mouse.get_pos()

            scrolled_save_button = save_name_button.copy()
            scrolled_save_button.y -= stats_scroll

            draw_button(
                scrolled_save_button,
                "SAVE",
                mouse_pos
            )

        unlocked_count = sum(
            1 for achievement in achievements.values()
            if achievement["unlocked"]
        )

        statistics = [
            ("TOTAL GEMS", str(total_gems)),
            ("TOTAL ROSES", str(total_roses)),
            ("ORB ACTIVATIONS", str(total_orb_activations)),
            ("RUNS PLAYED", str(runs_completed)),
            ("BEST COMBO", f"x{best_combo}"),
            (
                "ACHIEVEMENTS UNLOCKED",
                f"{unlocked_count}/{len(achievements)}"
            )
        ]

        stats_label_font = pygame.font.SysFont(
            "bahnschrift", 17, bold=True
        )

        stats_value_font = pygame.font.SysFont(
            "bahnschrift", 27, bold=True
        )

        card_width = 350
        card_height = 50

        start_x = 80
        start_y = 185

        horizontal_spacing = 390
        vertical_spacing = 56

        for i, (label, value) in enumerate(statistics):

            column = i % 2
            row = i // 2

            card_x = start_x + column * horizontal_spacing
            card_y = start_y + row * vertical_spacing

            card = pygame.Rect(
                card_x,
                card_y - stats_scroll,
                card_width,
                card_height
            )

            pygame.draw.rect(
                screen, (60, 35, 100), card, border_radius=10
            )

            pygame.draw.rect(
                screen, (110, 65, 160), card, 1, border_radius=10
            )

            label_text = stats_label_font.render(
                label,
                True,
                WHITE
            )

            screen.blit(
                label_text,
                (card_x + 12, card_y - stats_scroll + 14)
            )

            value_text = stats_value_font.render(
                value, True, CYAN
            )

            screen.blit(
                value_text,
                value_text.get_rect(
                    midright=(card.right - 12, card.centery)
                )
            )

        records_heading = button_font.render(
            "PERSONAL RECORDS",
            True,
            PINK
        )

        screen.blit(
            records_heading,
            records_heading.get_rect(
                center=(WIDTH // 2, 380 - stats_scroll)
            )
        )

        survival_minutes = best_survival_time // 60
        survival_seconds = best_survival_time % 60

        survival_text = (
            f"{survival_minutes:02d}:{survival_seconds:02d}"
        )

        personal_records = [
            ("HIGHEST SCORE", str(high_score)),
            ("LONGEST SURVIVAL", survival_text)
        ]

        record_label_font = pygame.font.SysFont(
            "bahnschrift", 17, bold=True
        )

        record_value_font = pygame.font.SysFont(
            "bahnschrift", 28, bold=True
        )

        record_width = 350
        record_height = 60
        record_y = 410

        for i, (label, value) in enumerate(personal_records):

            record_x = 80 + i * 390

            record_card = pygame.Rect(
                record_x,
                record_y - stats_scroll, 
                record_width,
                record_height
            )

            pygame.draw.rect(
                screen,
                (65, 40, 105),
                record_card,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                CYAN,
                record_card,
                2,
                border_radius=10
            )

            label_text = record_label_font.render(
                label,
                True,
                WHITE
            )

            screen.blit(
                label_text,
                (record_x + 12, record_y + 8 - stats_scroll)
            )

            value_text = record_value_font.render(
                value,
                True,
                YELLOW
            )

            screen.blit(
                value_text,
                (record_x + 12, record_y + 28 - stats_scroll)
            )

        screen.set_clip(None)

        mouse_pos = pygame.mouse.get_pos()

        draw_button(back_button, "BACK", mouse_pos)
        draw_button(reset_data_button, "RESET DATA", mouse_pos)

# confirm reset screen

    elif game_state == CONFIRM_RESET:
        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((10, 5, 30, 210))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(150, 125, 600, 250)

        pygame.draw.rect(
            screen,
            DARK_PURPLE,
            panel,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            PINK,
            panel,
            3,
            border_radius=20
        )

        heading = how_title_font.render(
            "RESET YOUR DATA",
            True,
            PINK
        )

        screen.blit(
            heading,
            heading.get_rect(
                center=(WIDTH // 2, 175)
            )
        )

        warning = small_font.render(
            "This will erase all your saved progress.",
            True,
            WHITE
        )

        screen.blit(
            warning,
            warning.get_rect(
                center=(WIDTH // 2, 225)
            )
        )

        reminder = instruction_font.render(
            "Your player name will not be kept!",
            True,
            CYAN
        )

        screen.blit(
            reminder,
            reminder.get_rect(
                center=(WIDTH // 2, 250)
            )
        )
        mouse_pos = pygame.mouse.get_pos()

        draw_button(
            confirm_reset_button,
            "RESET",
            mouse_pos
        )

        draw_button(
            cancel_reset_button,
            "CANCEL",
            mouse_pos
        )

    # page transi fade

    current_screen = (
        game_state,
        show_achievements,
        game_over
    )

    if current_screen != last_screen:

        last_screen = current_screen
        page_fade_alpha = 180

    else:

        page_fade_alpha = max(
            0, 
            page_fade_alpha - PAGE_FADE_SPEED
        )

    if page_fade_alpha > 0:

        fade_surface = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        fade_surface.fill(
            (10, 5, 30, page_fade_alpha)
        )

        screen.blit(fade_surface, (0, 0))

    if game_state == PLAYING and not game_over and not pause_menu_active:
        draw_pause_button(
            pause_button,
            pygame.mouse.get_pos()
        )

    if tutorial_active:
        draw_tutorial_overlay()


    if game_tutorial_active:
        panel = pygame.Rect(120, 20, 600, 100)

        pygame.draw.rect(
            screen, DARK_PURPLE, panel, border_radius=15
        )

        pygame.draw.rect(
            screen, CYAN, panel, 2, border_radius=15
        )

        tutorial_headings = [
            "1. LEARN TO JUMP",
            "2. COLLECT GEMS",
            "3. COLLECT ROSES",
            "4. ACTIVATE THE ORB",
            "5. USE THE JUMP PAD",
            "6. LEARN TO PAUSE",
            "7. YOU DID IT!"
        ]

        tutorial_instructions = [
            "Press SPACE or click to jump over the spike!",
            "Move into the floating gem to collect it.",
            "Collect the rose as you pass it.",
            "While airborne, pres SPACE or click near the orb.",
            "Land on the glowing pad. It will bounce you automatically!",
            "Click the pause button or press ESC to pause the game.",
            "You completed the practice course. Ready to play?"
        ]

        step = min(game_tutorial_step, len(tutorial_headings) - 1)

        heading = achievement_font.render(
            tutorial_headings[step],
            True, PINK
        )

        message = small_font.render(
            tutorial_instructions[step],
            True, WHITE
        )

        screen.blit(heading, (panel.x + 20, panel.y + 17))
        screen.blit(message, (panel.x + 20, panel.y + 57))

        if game_tutorial_step == 5:
            arrow_start = (780, 100)
            arrow_end = (pause_button.centerx, pause_button.centery + 15)

            arrow_color = CYAN
            arrow_width = 6
            arrow_size = 18

        else:
            arrow_start = (PLAYER_X + 65, 175)
            arrow_end = (PLAYER_X + 20, player.top - 10)

            arrow_color = PINK
            arrow_width = 4
            arrow_size = 12

        pygame.draw.line(
            screen,
            arrow_color,
            arrow_start,
            arrow_end,
            arrow_width
        )

        arrow_angle = math.atan2(
            arrow_end[1] - arrow_start[1],
            arrow_end[0] - arrow_start[0]
        )

        left = (
            arrow_end[0] - arrow_size * math.cos(arrow_angle - math.pi / 6),
            arrow_end[1] - arrow_size * math.sin(arrow_angle - math.pi / 6)

        )

        right = (
            arrow_end[0] - arrow_size * math.cos(arrow_angle + math.pi / 6),
            arrow_end[1] - arrow_size * math.sin(arrow_angle + math.pi / 6)
        )

        pygame.draw.polygon(
            screen,
            arrow_color,
            [arrow_end, left, right]
        )

        pygame.draw.polygon(
            screen, PINK,
            [
                arrow_end,
                (arrow_end[0] + 12, arrow_end[1] + 5),
                (arrow_end[0] + 5, arrow_end[1] + 14)
            ]
        )

        mouse_pos = pygame.mouse.get_pos()

        if game_tutorial_step == 5: 
            game_tutorial_skip_button.topleft = (25, 420)

        else:
            game_tutorial_skip_button.topleft = (730, 25)
        draw_button(
            game_tutorial_skip_button,
            "FINISH" if tutorial_finished else "SKIP",
            mouse_pos
        )

    if pause_menu_active:
        pause_overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        pause_overlay.fill((8, 4, 25, 175))
        screen.blit(pause_overlay, (0, 0))

        pause_panel = pygame.Rect(270, 35, 360, 440)

        glow_surface = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            glow_surface,
            (150, 60, 225, 35),
            pause_panel.inflate(18, 18),
            border_radius=32
        )

        screen.blit(glow_surface, (0, 0))

        shadow_rect = pause_panel.move(0, 7)

        pygame.draw.rect(
            screen,
            (8, 5, 25),
            shadow_rect,
            border_radius=25
        )

        pygame.draw.rect(
            screen,
            (27, 17, 58),
            pause_panel,
            border_radius=25
        )

        pygame.draw.rect(
            screen,
            (150, 75, 220),
            pause_panel,
            2,
            border_radius=25
        )

        inner_panel = pause_panel.inflate(-12, -12)

        pygame.draw.rect(
            screen, (75, 48, 120),
            inner_panel, 1, border_radius=20
        )

        pygame.draw.circle(
            screen,
            CYAN,
            (285, 88),
            3
        )

        pygame.draw.line(
            screen,
            (100, 65, 155),
            (320, 160),
            (580, 160),
            2
        )

        pause_shadow = title_font.render(
            "PAUSED",
            True,
            (75, 35, 110)
        )

        pause_title = title_font.render(
            "PAUSED",
            True,
            PINK
        )
        screen.blit(
            pause_shadow,
            pause_shadow.get_rect(
                center=(WIDTH // 2 + 2, 124)
            )
        )

        screen.blit(
            pause_title,
            pause_title.get_rect(
                center=(WIDTH // 2, 105)
            )
        )

        pause_subtitle = small_font.render(
            "TAKE A BREATHER, PLAYER",
            True,
            (190, 170, 220)
        )

        screen.blit(
            pause_subtitle,
            pause_subtitle.get_rect(
                center=(WIDTH // 2, 140)
            )
        )

        mouse_pos = pygame.mouse.get_pos()

        draw_button(resume_button, "RESUME", mouse_pos)
        draw_button(restart_button, "RESTART", mouse_pos)
        draw_button(pause_menu_button, "MAIN MENU", mouse_pos)
        draw_button(pause_quit_button, "QUIT GAME", mouse_pos)

        pause_hint = small_font.render(
            "PRESS ESC TO RESUME",
            True,
            (155, 135, 190)
        )

        screen.blit(
            pause_hint,
            pause_hint.get_rect(
                center=(WIDTH // 2, 445)
            )
        )


    pygame.display.flip()

pygame.quit()
