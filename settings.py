TITLE = "Jumpy Boi"
WIDTH = 500
HEIGHT = 500
FPS = 60
FONT_NAME = 'impact'
HS_FILE = "highscore.txt"
SPRITESHEET = "Spritesheet.png"

PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

JETPACK_POWER = 50
JETPACK_SPAWN_RATE = 7

PLATFORM_LIST = [(225, HEIGHT - 20),
                 (WIDTH - 125, HEIGHT / 2),
                 (75, HEIGHT / 2),
                 (225, HEIGHT / 4)]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIGHTBLUE = (0, 155, 200)
BGCOLOR = LIGHTBLUE