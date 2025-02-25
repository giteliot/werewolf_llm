WIDTH, HEIGHT = 16*60, 12*60

TBOX_WIDTH = 300
TBOX_HEIGHT = 280

NBOX_WIDTH = 500
NBOX_HEIGHT = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (30, 30, 30)
PLAYER_COLOR = (70, 130, 180)
BOX_COLOR = (50, 50, 50)
FONT_SIZE = 20

PLAYER_RADIUS = 40

player_positions = {
    "deepseek": (280, 400),
    "grok": (480, 350),
    "gemini": (360, 540),
    "gpt4": (670, 400),
    "sonnet": (600, 540)
}

text_positions = {
    "deepseek": (10, 10),
    "grok": (WIDTH//2-TBOX_WIDTH//2, 10),
    "sonnet": (WIDTH-TBOX_WIDTH-10,  HEIGHT-TBOX_HEIGHT-10),
    "gemini": (10, HEIGHT-TBOX_HEIGHT-10),
    "gpt4": (WIDTH-TBOX_WIDTH-10, 10)
}