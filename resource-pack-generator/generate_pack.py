#!/usr/bin/env python3
"""
Purple Galaxy Minecraft Resource Pack Generator
Generates all textures and packages them as ZIP files for multiple MC versions.
"""

import json
import math
import os
import random
import zipfile
from io import BytesIO

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ── Color palette ──────────────────────────────────────────────────────────
PURPLE_DARK = (60, 10, 90)
PURPLE_MID = (120, 40, 180)
PURPLE_LIGHT = (180, 100, 255)
PURPLE_GLOW = (200, 140, 255)
GALAXY_DARK = (15, 5, 30)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "website", "downloads")
PACK_NAME = "PurpleGalaxy"


# ── Helper functions ───────────────────────────────────────────────────────

def lerp_color(c1, c2, t):
    """Linear interpolation between two RGB(A) colors."""
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def draw_pixel_rect(draw, x, y, w, h, color):
    """Draw a filled rectangle (pixel art style)."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=color)


def create_gradient(width, height, color_top, color_bottom):
    """Create a vertical gradient image."""
    img = Image.new("RGBA", (width, height))
    for y in range(height):
        t = y / max(height - 1, 1)
        color = lerp_color(color_top, color_bottom, t)
        for x in range(width):
            img.putpixel((x, y), color + (255,) if len(color) == 3 else color)
    return img


def add_stars(img, count=100, seed=42):
    """Add random stars to an image."""
    rng = random.Random(seed)
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for _ in range(count):
        x = rng.randint(0, w - 1)
        y = rng.randint(0, h - 1)
        brightness = rng.randint(180, 255)
        size = rng.choice([1, 1, 1, 2])
        color = (brightness, brightness, rng.randint(brightness, 255), rng.randint(150, 255))
        if size == 1:
            img.putpixel((x, y), color)
        else:
            draw.ellipse([x, y, x + size, y + size], fill=color)
    return img


def add_nebula(img, seed=42):
    """Add a subtle nebula effect."""
    rng = random.Random(seed)
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for _ in range(5):
        cx = rng.randint(0, w)
        cy = rng.randint(0, h)
        r = rng.randint(w // 6, w // 3)
        color = (
            rng.randint(80, 160),
            rng.randint(20, 80),
            rng.randint(150, 255),
            rng.randint(15, 40),
        )
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=max(w // 8, 3)))
    return Image.alpha_composite(img, overlay)


# ── Texture generators ─────────────────────────────────────────────────────

def generate_pack_png():
    """Generate the resource pack icon (128x128)."""
    size = 128
    img = Image.new("RGBA", (size, size), GALAXY_DARK + (255,))
    img = add_nebula(img, seed=99)
    img = add_stars(img, count=60, seed=99)
    draw = ImageDraw.Draw(img)

    # Draw a large purple "P" in pixel art style
    # Border
    border_color = PURPLE_LIGHT + (255,)
    draw.rectangle([10, 10, size - 11, size - 11], outline=border_color, width=3)

    # Letter P made of blocks
    p_color = PURPLE_GLOW + (255,)
    p_x, p_y = 30, 25
    block = 8
    # Vertical bar
    for i in range(9):
        draw_pixel_rect(draw, p_x, p_y + i * block, block, block, p_color)
    # Top horizontal
    for i in range(1, 5):
        draw_pixel_rect(draw, p_x + i * block, p_y, block, block, p_color)
    # Right vertical (top part)
    for i in range(1, 4):
        draw_pixel_rect(draw, p_x + 5 * block, p_y + i * block, block, block, p_color)
    # Middle horizontal
    for i in range(1, 5):
        draw_pixel_rect(draw, p_x + i * block, p_y + 4 * block, block, block, p_color)

    # Add "Purple" text at bottom
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    draw.text((size // 2, size - 22), "GALAXY", fill=PURPLE_LIGHT + (255,), font=font, anchor="mm")

    return img


def generate_crosshair():
    """Generate a round purple translucent crosshair (15x15)."""
    size = 15
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = size // 2

    # Outer ring
    draw.ellipse([1, 1, size - 2, size - 2], outline=PURPLE_LIGHT + (140,), width=1)
    # Inner fill - very faint purple
    draw.ellipse([3, 3, size - 4, size - 4], fill=(160, 80, 220, 35))
    # Center dot
    img.putpixel((center, center), PURPLE_GLOW + (180,))
    # Cross lines (thin)
    for i in [center - 1, center + 1]:
        img.putpixel((i, center), PURPLE_LIGHT + (120,))
        img.putpixel((center, i), PURPLE_LIGHT + (120,))

    return img


def generate_heart_full():
    """Generate a purple heart (9x9) - full heart."""
    img = Image.new("RGBA", (9, 9), (0, 0, 0, 0))
    # Heart shape pixel map (9x9)
    heart = [
        [0, 1, 1, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    # Highlight map for 3D effect
    highlight = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 2, 0, 0, 0, 2, 0, 0],
        [0, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    for y in range(9):
        for x in range(9):
            if heart[y][x]:
                if highlight[y][x] == 2:
                    img.putpixel((x, y), PURPLE_GLOW + (255,))
                else:
                    img.putpixel((x, y), PURPLE_MID + (255,))

    # Dark outline
    outline_color = PURPLE_DARK + (255,)
    outline_pixels = [
        (1, 0), (2, 0), (6, 0), (7, 0),
        (0, 1), (4, 0), (4, 1),
        (0, 2), (8, 1), (8, 2),
        (0, 3), (8, 3),
    ]
    for px, py in outline_pixels:
        img.putpixel((px, py), outline_color)

    return img


def generate_heart_half():
    """Generate a half purple heart (9x9)."""
    img = Image.new("RGBA", (9, 9), (0, 0, 0, 0))
    heart = [
        [0, 1, 1, 0, 0, 0, 1, 1, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    for y in range(9):
        for x in range(9):
            if heart[y][x]:
                if x < 5:
                    img.putpixel((x, y), PURPLE_MID + (255,))
                else:
                    img.putpixel((x, y), (40, 10, 60, 200))
    return img


def generate_heart_container():
    """Generate a heart container outline (9x9)."""
    img = Image.new("RGBA", (9, 9), (0, 0, 0, 0))
    heart = [
        [0, 1, 1, 0, 0, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    for y in range(9):
        for x in range(9):
            if heart[y][x]:
                img.putpixel((x, y), (40, 10, 60, 255))
    return img


def generate_hotbar():
    """Generate a purple hotbar (182x22)."""
    w, h = 182, 22
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background - dark purple with slight transparency
    draw.rectangle([0, 0, w - 1, h - 1], fill=(30, 8, 50, 200))

    # Border
    draw.rectangle([0, 0, w - 1, h - 1], outline=(100, 40, 160, 255), width=1)
    # Inner border highlight
    draw.rectangle([1, 1, w - 2, h - 2], outline=(60, 20, 100, 180), width=1)

    # Slot dividers - 9 slots, each 20px wide
    for i in range(1, 9):
        x = 2 + i * 20
        draw.line([(x, 2), (x, h - 3)], fill=(80, 30, 130, 150), width=1)

    # Slot backgrounds - subtle galaxy effect
    for slot in range(9):
        sx = 3 + slot * 20
        sy = 3
        sw, sh = 18, 16
        for y in range(sy, sy + sh):
            for x in range(sx, sx + sw):
                t = (y - sy) / sh
                base = lerp_color((20, 5, 35), (35, 12, 55), t)
                img.putpixel((x, y), base + (180,))

    return img


def generate_hotbar_selection():
    """Generate a purple hotbar selection indicator (24x24)."""
    size = 24
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer glow
    draw.rectangle([0, 0, size - 1, size - 1], outline=PURPLE_GLOW + (200,), width=2)
    # Inner highlight
    draw.rectangle([2, 2, size - 3, size - 3], outline=PURPLE_LIGHT + (150,), width=1)

    return img


def generate_inventory():
    """Generate a galaxy-themed inventory (176x166)."""
    w, h = 176, 166
    img = Image.new("RGBA", (w, h), GALAXY_DARK + (255,))

    # Add galaxy background
    img = add_nebula(img, seed=77)
    img = add_stars(img, count=80, seed=77)

    draw = ImageDraw.Draw(img)

    # Semi-transparent overlay for readability
    overlay = Image.new("RGBA", (w, h), (15, 5, 30, 140))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Border
    draw.rectangle([0, 0, w - 1, h - 1], outline=PURPLE_LIGHT + (220,), width=2)
    draw.rectangle([2, 2, w - 3, h - 3], outline=PURPLE_DARK + (200,), width=1)

    # Title area
    draw.rectangle([6, 4, w - 7, 16], fill=(30, 10, 50, 180))

    slot_bg = (25, 8, 40, 200)
    slot_border = (80, 30, 130, 180)
    slot_size = 16

    def draw_slot(x, y):
        draw.rectangle([x, y, x + slot_size + 1, y + slot_size + 1], fill=slot_bg)
        draw.rectangle([x, y, x + slot_size + 1, y + slot_size + 1], outline=slot_border)
        # Highlight top-left
        draw.line([(x + 1, y + 1), (x + slot_size, y + 1)], fill=(50, 18, 80, 120))
        draw.line([(x + 1, y + 1), (x + 1, y + slot_size)], fill=(50, 18, 80, 120))

    # Crafting grid (2x2) - top right area
    craft_x, craft_y = 98, 18
    for row in range(2):
        for col in range(2):
            draw_slot(craft_x + col * 18, craft_y + row * 18)

    # Crafting output
    draw_slot(craft_x + 56, craft_y + 9)

    # Arrow
    arrow_x = craft_x + 38
    arrow_y = craft_y + 12
    draw.polygon([(arrow_x, arrow_y), (arrow_x + 12, arrow_y + 6),
                  (arrow_x, arrow_y + 12)], fill=PURPLE_MID + (200,))

    # Player armor slots (4 slots on left)
    for i in range(4):
        draw_slot(7, 18 + i * 18)

    # Player model area (center)
    player_x, player_y = 51, 18
    draw.rectangle([player_x, player_y, player_x + 36, player_y + 54],
                   fill=(20, 5, 35, 150), outline=slot_border)

    # Shield/offhand slot
    draw_slot(76, 61)

    # Main inventory (3 rows x 9 cols)
    inv_y = 84
    for row in range(3):
        for col in range(9):
            draw_slot(7 + col * 18, inv_y + row * 18)

    # Hotbar (1 row x 9 cols)
    hotbar_y = 142
    for col in range(9):
        draw_slot(7 + col * 18, hotbar_y)

    # Separator line
    draw.line([(7, inv_y - 2), (w - 8, inv_y - 2)], fill=PURPLE_MID + (100,))
    draw.line([(7, hotbar_y - 2), (w - 8, hotbar_y - 2)], fill=PURPLE_MID + (100,))

    return img


def generate_sky_texture():
    """Generate a purple/violet sky texture for OptiFine (256x256)."""
    size = 256
    img = create_gradient(size, size,
                          (40, 10, 80, 255),
                          (100, 30, 160, 255))
    img = add_nebula(img, seed=55)
    img = add_stars(img, count=200, seed=55)
    return img


def generate_sky_properties():
    """Generate OptiFine sky properties file."""
    return """source=sky1.png
startFadeIn=18:00
endFadeIn=19:00
startFadeOut=5:00
endFadeOut=6:00
blend=add
rotate=true
speed=1.0
axis=0.0 0.0 1.0
"""


def generate_sun():
    """Generate a purple-tinted sun (32x32)."""
    size = 32
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    center = size // 2

    # Outer glow
    for r in range(center, 4, -1):
        alpha = int(40 * (1 - r / center))
        color = (200, 150, 255, alpha)
        draw.ellipse([center - r, center - r, center + r, center + r], fill=color)

    # Core
    draw.ellipse([center - 6, center - 6, center + 6, center + 6],
                 fill=(255, 220, 255, 240))
    draw.ellipse([center - 4, center - 4, center + 4, center + 4],
                 fill=(255, 240, 255, 255))

    return img


def generate_moon_phases():
    """Generate purple-tinted moon phases (128x32 - 4 phases of 32x32)."""
    w, h = 128, 32
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for phase in range(4):
        cx = phase * 32 + 16
        cy = 16

        # Moon base
        draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10],
                     fill=(200, 170, 230, 255))

        # Phase shadow
        if phase > 0:
            offset = (phase / 3) * 12
            draw.ellipse([cx - 10 + int(offset), cy - 10,
                         cx + 10 + int(offset), cy + 10],
                        fill=(0, 0, 0, 0))

        # Craters
        rng = random.Random(phase + 100)
        for _ in range(3):
            dx = rng.randint(-6, 6)
            dy = rng.randint(-6, 6)
            r = rng.randint(1, 3)
            draw.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                         fill=(170, 140, 200, 200))

    return img


def generate_clouds():
    """Generate purple-tinted clouds texture (256x256)."""
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    rng = random.Random(123)
    for _ in range(30):
        x = rng.randint(0, size)
        y = rng.randint(0, size)
        w = rng.randint(20, 60)
        h = rng.randint(10, 25)
        alpha = rng.randint(60, 140)
        color = (180, 140, 220, alpha)
        draw.ellipse([x, y, x + w, y + h], fill=color)

    img = img.filter(ImageFilter.GaussianBlur(radius=3))
    return img


# ── Item texture generators ──────────────────────────────────────────────

def generate_sword():
    """Generate a purple sword (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    # Sword pixel art - diagonal blade
    pixels = {
        # Handle
        (3, 13): (80, 40, 20, 255),
        (4, 12): (80, 40, 20, 255),
        # Guard
        (3, 11): PURPLE_DARK + (255,),
        (4, 11): PURPLE_DARK + (255,),
        (5, 11): PURPLE_DARK + (255,),
        (6, 11): PURPLE_DARK + (255,),
        # Blade
        (5, 10): PURPLE_MID + (255,),
        (6, 9): PURPLE_MID + (255,),
        (7, 8): PURPLE_LIGHT + (255,),
        (8, 7): PURPLE_LIGHT + (255,),
        (9, 6): PURPLE_LIGHT + (255,),
        (10, 5): PURPLE_GLOW + (255,),
        (11, 4): PURPLE_GLOW + (255,),
        (12, 3): PURPLE_GLOW + (255,),
        (13, 2): PURPLE_LIGHT + (255,),
        # Blade edge (lighter)
        (6, 10): PURPLE_GLOW + (255,),
        (7, 9): PURPLE_GLOW + (255,),
        (8, 8): PURPLE_GLOW + (200,),
        (9, 7): (220, 180, 255, 255),
        (10, 6): (220, 180, 255, 255),
        (11, 5): (230, 200, 255, 255),
        (12, 4): (230, 200, 255, 255),
        # Pommel
        (2, 14): (60, 30, 15, 255),
    }
    for (x, y), color in pixels.items():
        img.putpixel((x, y), color)
    return img


def generate_pickaxe():
    """Generate a purple pickaxe (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    handle_color = (100, 60, 30, 255)
    head_color = PURPLE_MID + (255,)
    highlight = PURPLE_GLOW + (255,)

    pixels = {
        # Handle (diagonal)
        (4, 12): handle_color, (5, 11): handle_color,
        (6, 10): handle_color, (7, 9): handle_color,
        (8, 8): handle_color,
        # Head
        (6, 5): head_color, (7, 4): head_color,
        (8, 3): head_color, (9, 2): head_color,
        (10, 3): head_color, (11, 4): head_color,
        (9, 6): head_color, (10, 5): head_color,
        (11, 6): head_color,
        # Highlights
        (7, 5): highlight, (8, 4): highlight,
        (9, 3): highlight, (10, 4): highlight,
    }
    for (x, y), color in pixels.items():
        img.putpixel((x, y), color)
    return img


def generate_axe():
    """Generate a purple axe (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    handle_color = (100, 60, 30, 255)
    head_color = PURPLE_MID + (255,)
    highlight = PURPLE_GLOW + (255,)

    pixels = {
        # Handle
        (4, 13): handle_color, (5, 12): handle_color,
        (6, 11): handle_color, (7, 10): handle_color,
        (8, 9): handle_color,
        # Axe head
        (8, 5): head_color, (9, 4): head_color,
        (10, 3): head_color, (10, 4): head_color,
        (10, 5): head_color, (11, 4): head_color,
        (11, 5): head_color, (11, 6): head_color,
        (9, 6): head_color, (9, 7): head_color,
        (10, 6): head_color, (10, 7): head_color,
        (9, 8): head_color,
        # Highlights
        (9, 5): highlight, (10, 4): highlight,
        (11, 5): highlight,
    }
    for (x, y), color in pixels.items():
        img.putpixel((x, y), color)
    return img


def generate_shovel():
    """Generate a purple shovel (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    handle_color = (100, 60, 30, 255)
    head_color = PURPLE_MID + (255,)
    highlight = PURPLE_GLOW + (255,)

    pixels = {
        # Handle
        (5, 13): handle_color, (6, 12): handle_color,
        (7, 11): handle_color, (8, 10): handle_color,
        (9, 9): handle_color, (10, 8): handle_color,
        # Shovel head
        (10, 5): head_color, (11, 4): head_color,
        (10, 4): head_color, (11, 3): head_color,
        (11, 5): head_color, (12, 4): head_color,
        (10, 6): head_color, (11, 6): head_color,
        (10, 7): head_color, (11, 7): head_color,
        # Highlights
        (10, 4): highlight, (11, 3): highlight,
    }
    for (x, y), color in pixels.items():
        img.putpixel((x, y), color)
    return img


def generate_apple():
    """Generate a purple apple (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    body = PURPLE_MID + (255,)
    dark = PURPLE_DARK + (255,)
    light = PURPLE_LIGHT + (255,)
    stem = (80, 50, 30, 255)
    leaf = (100, 40, 140, 255)

    apple_shape = [
        "................",
        "......S.........",
        ".....SL.........",
        "....LLLL........",
        "...BBBBBB.......",
        "..BBBHBBBB......",
        "..BBHHBBBB......",
        "..BBBHBBBB......",
        "..BBBBBBBB......",
        "..BBBBBBB.......",
        "...BDBBBBB......",
        "...BBDDBB.......",
        "....BDDB........",
        "................",
        "................",
        "................",
    ]
    color_map = {"B": body, "D": dark, "H": light, "S": stem, "L": leaf}
    for y, row in enumerate(apple_shape):
        for x, ch in enumerate(row):
            if ch in color_map:
                img.putpixel((x, y), color_map[ch])
    return img


def generate_diamond():
    """Generate a purple gem/diamond (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    dark = PURPLE_DARK + (255,)
    mid = PURPLE_MID + (255,)
    light = PURPLE_LIGHT + (255,)
    glow = PURPLE_GLOW + (255,)

    gem_shape = [
        "................",
        "................",
        "................",
        "....MMMMMM.....",
        "...MLLLLLGM....",
        "..MLLGGGGLGM...",
        "..MLGGGGGLGM...",
        "...MGGGGGMM....",
        "...MMGGGMM.....",
        "....MMGMM......",
        "....MMMM.......",
        ".....MM.........",
        "................",
        "................",
        "................",
        "................",
    ]
    color_map = {"M": mid, "L": light, "G": glow, "D": dark}
    for y, row in enumerate(gem_shape):
        for x, ch in enumerate(row):
            if ch in color_map:
                img.putpixel((x, y), color_map[ch])
    return img


def generate_ender_pearl():
    """Generate a purple ender pearl (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer sphere
    draw.ellipse([3, 3, 12, 12], fill=PURPLE_DARK + (255,))
    draw.ellipse([4, 4, 11, 11], fill=PURPLE_MID + (255,))
    # Highlight
    draw.ellipse([5, 5, 8, 8], fill=PURPLE_LIGHT + (200,))
    # Center eye
    img.putpixel((7, 7), PURPLE_GLOW + (255,))
    img.putpixel((8, 7), (220, 180, 255, 255))

    return img


def generate_potion():
    """Generate a purple potion (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    glass = (200, 170, 230, 180)
    liquid = PURPLE_MID + (220,)
    cork = (140, 100, 60, 255)

    # Cork
    draw.rectangle([6, 1, 9, 3], fill=cork)
    # Neck
    draw.rectangle([6, 4, 9, 6], fill=glass)
    # Body
    draw.rectangle([4, 7, 11, 13], fill=glass)
    # Liquid
    draw.rectangle([5, 9, 10, 12], fill=liquid)
    # Highlight
    draw.line([(5, 8), (5, 12)], fill=PURPLE_GLOW + (120,))

    return img


def generate_ingot():
    """Generate a purple ingot (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    dark = PURPLE_DARK + (255,)
    mid = PURPLE_MID + (255,)
    light = PURPLE_LIGHT + (255,)

    ingot_shape = [
        "................",
        "................",
        "................",
        "................",
        "................",
        "...LLLLLLLL.....",
        "..LLLLLLLLLM....",
        "..LMMMMMMMMM....",
        "..MMMMMMMMMD....",
        "..MDDDDDDDD....",
        "...DDDDDDDD.....",
        "................",
        "................",
        "................",
        "................",
        "................",
    ]
    color_map = {"L": light, "M": mid, "D": dark}
    for y, row in enumerate(ingot_shape):
        for x, ch in enumerate(row):
            if ch in color_map:
                img.putpixel((x, y), color_map[ch])
    return img


def generate_bow():
    """Generate a purple bow (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    wood = (80, 30, 100, 255)
    string_c = (200, 170, 230, 255)

    pixels = {
        # Bow curve
        (6, 1): wood, (5, 2): wood, (4, 3): wood,
        (3, 4): wood, (3, 5): wood, (3, 6): wood,
        (3, 7): wood, (3, 8): wood, (3, 9): wood,
        (3, 10): wood, (4, 11): wood, (5, 12): wood,
        (6, 13): wood,
        # String
        (7, 1): string_c, (7, 2): string_c,
        (7, 3): string_c, (7, 4): string_c,
        (7, 5): string_c, (7, 6): string_c,
        (7, 7): string_c, (7, 8): string_c,
        (7, 9): string_c, (7, 10): string_c,
        (7, 11): string_c, (7, 12): string_c,
        (7, 13): string_c,
    }
    for (x, y), color in pixels.items():
        img.putpixel((x, y), color)
    return img


def generate_arrow():
    """Generate a purple arrow (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    shaft = (100, 60, 30, 255)
    tip = PURPLE_LIGHT + (255,)
    feather = PURPLE_MID + (255,)

    pixels = {
        # Tip
        (12, 2): tip, (13, 1): tip, (11, 3): tip,
        # Shaft
        (10, 4): shaft, (9, 5): shaft, (8, 6): shaft,
        (7, 7): shaft, (6, 8): shaft, (5, 9): shaft,
        (4, 10): shaft, (3, 11): shaft,
        # Feathers
        (2, 12): feather, (1, 13): feather,
        (3, 13): feather, (2, 14): feather,
        (1, 12): feather,
    }
    for (x, y), color in pixels.items():
        img.putpixel((x, y), color)
    return img


def generate_block_texture(name="generic"):
    """Generate a purple block item texture (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    rng = random.Random(hash(name))
    base_r = rng.randint(60, 140)
    base_g = rng.randint(20, 60)
    base_b = rng.randint(120, 200)

    # Fill with slightly varied purple
    for y in range(16):
        for x in range(16):
            variation = rng.randint(-15, 15)
            r = max(0, min(255, base_r + variation))
            g = max(0, min(255, base_g + variation))
            b = max(0, min(255, base_b + variation))
            img.putpixel((x, y), (r, g, b, 255))

    # Add border lines for block texture feel
    draw.line([(0, 0), (15, 0)], fill=(base_r + 30, base_g + 15, base_b + 20, 255))
    draw.line([(0, 0), (0, 15)], fill=(base_r + 30, base_g + 15, base_b + 20, 255))
    draw.line([(15, 0), (15, 15)], fill=(base_r - 30, base_g - 10, base_b - 20, 255))
    draw.line([(0, 15), (15, 15)], fill=(base_r - 30, base_g - 10, base_b - 20, 255))

    return img


def generate_food_item(name="generic"):
    """Generate a purple food item (16x16)."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    rng = random.Random(hash(name))

    base = (rng.randint(100, 160), rng.randint(30, 70), rng.randint(140, 220))
    dark = tuple(max(0, c - 40) for c in base)
    light = tuple(min(255, c + 40) for c in base)

    # Simple rounded shape
    for y in range(4, 13):
        for x in range(4, 13):
            dist = math.sqrt((x - 8) ** 2 + (y - 8.5) ** 2)
            if dist < 4.5:
                t = dist / 4.5
                color = lerp_color(light, dark, t)
                img.putpixel((x, y), color + (255,))

    return img


# ── Icons.png for pre-1.20.2 ──────────────────────────────────────────────

def generate_icons_png():
    """Generate the classic icons.png sprite sheet (256x256) with purple theme."""
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

    # Crosshair at (0,0) - 16x16 area, crosshair is centered
    crosshair = generate_crosshair()
    # Place crosshair centered in the 16x16 area
    cx = (16 - crosshair.width) // 2
    cy = (16 - crosshair.height) // 2
    img.paste(crosshair, (cx, cy), crosshair)

    # Hearts - Row at y=0, starting at x=16
    # Container hearts (outline)
    container = generate_heart_container()
    img.paste(container, (16, 0), container)

    # Full heart at various positions
    full = generate_heart_full()
    img.paste(full, (52, 0), full)  # Normal full heart
    img.paste(full, (16 + 9 * 4, 0), full)

    # Half heart
    half = generate_heart_half()
    img.paste(half, (61, 0), half)

    # Row 1 (y=9) - hardcore hearts (same but with different container)
    img.paste(container, (16, 9), container)
    img.paste(full, (52, 9), full)
    img.paste(half, (61, 9), half)

    # Armor icons at y=9 - use purple tinted
    # Experience bar background
    draw = ImageDraw.Draw(img)

    # Hunger icons y=27 - purple themed
    hunger_full = generate_heart_full()  # Reuse heart shape for hunger
    img.paste(hunger_full, (52, 27), hunger_full)

    # Air bubbles y=18
    bubble_color = PURPLE_LIGHT + (200,)
    draw.ellipse([16, 18, 24, 26], fill=bubble_color, outline=PURPLE_DARK + (255,))

    return img


def generate_widgets_png():
    """Generate the classic widgets.png sprite sheet (256x256) with purple theme."""
    img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))

    # Hotbar at (0, 0)
    hotbar = generate_hotbar()
    img.paste(hotbar, (0, 0), hotbar)

    # Hotbar selection at (0, 22)
    selection = generate_hotbar_selection()
    img.paste(selection, (0, 22), selection)

    # Experience bar empty at (0, 64) - 182x5
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 64, 181, 68], fill=(30, 10, 50, 255),
                   outline=PURPLE_DARK + (255,))

    # Experience bar full at (0, 69) - 182x5
    draw.rectangle([0, 69, 181, 73], fill=PURPLE_MID + (255,),
                   outline=PURPLE_DARK + (255,))

    # Buttons
    # Normal button at (0, 46) - 200x20
    draw.rectangle([0, 46, 199, 65], fill=(40, 15, 65, 255),
                   outline=PURPLE_MID + (255,))
    # Hover button at (0, 86) - 200x20
    draw.rectangle([0, 86, 199, 105], fill=(60, 25, 100, 255),
                   outline=PURPLE_LIGHT + (255,))

    return img


# ── Pack assembly ──────────────────────────────────────────────────────────

# MC version to pack_format mapping
VERSION_FORMATS = {
    "1.16.x": 6,
    "1.17.x": 7,
    "1.18.x": 9,
    "1.19.x": 13,
    "1.20-1.20.1": 15,
    "1.20.2-1.20.4": 18,
    "1.20.5-1.20.6": 32,
    "1.21-1.21.1": 34,
    "1.21.2-1.21.4": 42,
}

# Item textures to include
ITEM_GENERATORS = {
    "diamond_sword": generate_sword,
    "diamond_pickaxe": generate_pickaxe,
    "diamond_axe": generate_axe,
    "diamond_shovel": generate_shovel,
    "iron_sword": generate_sword,
    "iron_pickaxe": generate_pickaxe,
    "iron_axe": generate_axe,
    "iron_shovel": generate_shovel,
    "golden_sword": generate_sword,
    "golden_pickaxe": generate_pickaxe,
    "golden_axe": generate_axe,
    "golden_shovel": generate_shovel,
    "netherite_sword": generate_sword,
    "netherite_pickaxe": generate_pickaxe,
    "netherite_axe": generate_axe,
    "netherite_shovel": generate_shovel,
    "stone_sword": generate_sword,
    "stone_pickaxe": generate_pickaxe,
    "stone_axe": generate_axe,
    "stone_shovel": generate_shovel,
    "wooden_sword": generate_sword,
    "wooden_pickaxe": generate_pickaxe,
    "wooden_axe": generate_axe,
    "wooden_shovel": generate_shovel,
    "apple": generate_apple,
    "golden_apple": generate_apple,
    "enchanted_golden_apple": generate_apple,
    "diamond": generate_diamond,
    "emerald": generate_diamond,
    "ender_pearl": generate_ender_pearl,
    "ender_eye": generate_ender_pearl,
    "potion": generate_potion,
    "bow": generate_bow,
    "arrow": generate_arrow,
    "iron_ingot": generate_ingot,
    "gold_ingot": generate_ingot,
    "netherite_ingot": generate_ingot,
    "copper_ingot": generate_ingot,
}

# Block textures
BLOCK_TEXTURES = [
    "stone", "dirt", "grass_block_top", "grass_block_side",
    "cobblestone", "oak_planks", "spruce_planks", "birch_planks",
    "oak_log", "oak_log_top", "glass", "sand",
    "gravel", "iron_ore", "gold_ore", "diamond_ore",
    "coal_ore", "obsidian", "bedrock", "netherrack",
    "end_stone", "purpur_block", "amethyst_block",
]

# Food items
FOOD_ITEMS = [
    "cooked_beef", "cooked_porkchop", "cooked_chicken",
    "cooked_mutton", "bread", "cookie", "cake",
    "pumpkin_pie", "melon_slice", "sweet_berries",
    "cooked_cod", "cooked_salmon",
]


def build_pack(version_name, pack_format):
    """Build a complete resource pack ZIP for a given MC version."""
    print(f"  Building pack for {version_name} (format {pack_format})...")

    zip_buffer = BytesIO()
    uses_sprites = pack_format >= 18  # 1.20.2+

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # pack.mcmeta
        pack_meta = {
            "pack": {
                "pack_format": pack_format,
                "description": "\u00a75\u00a7l Purple Galaxy \u00a7r\u00a7d Resource Pack\n\u00a77A violet dream for Minecraft"
            }
        }
        zf.writestr("pack.mcmeta", json.dumps(pack_meta, indent=2))

        # pack.png
        pack_icon = generate_pack_png()
        icon_buf = BytesIO()
        pack_icon.save(icon_buf, "PNG")
        zf.writestr("pack.png", icon_buf.getvalue())

        # ── GUI textures ──
        if uses_sprites:
            # New sprite system (1.20.2+)
            sprite_base = "assets/minecraft/textures/gui/sprites/hud"

            # Crosshair
            crosshair = generate_crosshair()
            buf = BytesIO()
            crosshair.save(buf, "PNG")
            zf.writestr(f"{sprite_base}/crosshair.png", buf.getvalue())

            # Hotbar
            hotbar = generate_hotbar()
            buf = BytesIO()
            hotbar.save(buf, "PNG")
            zf.writestr(f"{sprite_base}/hotbar.png", buf.getvalue())

            # Hotbar selection
            selection = generate_hotbar_selection()
            buf = BytesIO()
            selection.save(buf, "PNG")
            zf.writestr(f"{sprite_base}/hotbar_selection.png", buf.getvalue())

            # Hearts
            heart_base = f"{sprite_base}/heart"
            for name, gen_func in [
                ("full", generate_heart_full),
                ("full_blinking", generate_heart_full),
                ("half", generate_heart_half),
                ("half_blinking", generate_heart_half),
                ("container", generate_heart_container),
                ("container_blinking", generate_heart_container),
            ]:
                heart_img = gen_func()
                buf = BytesIO()
                heart_img.save(buf, "PNG")
                zf.writestr(f"{heart_base}/{name}.png", buf.getvalue())

            # Experience bar
            exp_empty = Image.new("RGBA", (182, 5), (30, 10, 50, 255))
            ImageDraw.Draw(exp_empty).rectangle([0, 0, 181, 4],
                                                 outline=PURPLE_DARK + (255,))
            buf = BytesIO()
            exp_empty.save(buf, "PNG")
            zf.writestr(f"{sprite_base}/experience_bar_background.png", buf.getvalue())

            exp_full = Image.new("RGBA", (182, 5), PURPLE_MID + (255,))
            ImageDraw.Draw(exp_full).rectangle([0, 0, 181, 4],
                                                outline=PURPLE_DARK + (255,))
            buf = BytesIO()
            exp_full.save(buf, "PNG")
            zf.writestr(f"{sprite_base}/experience_bar_progress.png", buf.getvalue())

        else:
            # Old sprite sheet system (pre-1.20.2)
            gui_base = "assets/minecraft/textures/gui"

            icons = generate_icons_png()
            buf = BytesIO()
            icons.save(buf, "PNG")
            zf.writestr(f"{gui_base}/icons.png", buf.getvalue())

            widgets = generate_widgets_png()
            buf = BytesIO()
            widgets.save(buf, "PNG")
            zf.writestr(f"{gui_base}/widgets.png", buf.getvalue())

        # ── Inventory ──
        inventory = generate_inventory()
        buf = BytesIO()
        inventory.save(buf, "PNG")
        zf.writestr("assets/minecraft/textures/gui/container/inventory.png",
                     buf.getvalue())

        # ── Environment ──
        env_base = "assets/minecraft/textures/environment"

        # Sun
        sun = generate_sun()
        buf = BytesIO()
        sun.save(buf, "PNG")
        zf.writestr(f"{env_base}/sun.png", buf.getvalue())

        # Moon phases
        moon = generate_moon_phases()
        buf = BytesIO()
        moon.save(buf, "PNG")
        zf.writestr(f"{env_base}/moon_phases.png", buf.getvalue())

        # Clouds
        clouds = generate_clouds()
        buf = BytesIO()
        clouds.save(buf, "PNG")
        zf.writestr(f"{env_base}/clouds.png", buf.getvalue())

        # End sky
        end_sky = generate_sky_texture()
        buf = BytesIO()
        end_sky.save(buf, "PNG")
        zf.writestr(f"{env_base}/end_sky.png", buf.getvalue())

        # ── OptiFine sky ──
        optifine_base = "assets/minecraft/optifine/sky/world0"

        sky_tex = generate_sky_texture()
        buf = BytesIO()
        sky_tex.save(buf, "PNG")
        zf.writestr(f"{optifine_base}/sky1.png", buf.getvalue())
        zf.writestr(f"{optifine_base}/sky1.properties",
                    generate_sky_properties())

        # ── Item textures ──
        item_base = "assets/minecraft/textures/item"

        for item_name, gen_func in ITEM_GENERATORS.items():
            item_img = gen_func()
            buf = BytesIO()
            item_img.save(buf, "PNG")
            zf.writestr(f"{item_base}/{item_name}.png", buf.getvalue())

        # Food items
        for food_name in FOOD_ITEMS:
            food_img = generate_food_item(food_name)
            buf = BytesIO()
            food_img.save(buf, "PNG")
            zf.writestr(f"{item_base}/{food_name}.png", buf.getvalue())

        # ── Block textures ──
        block_base = "assets/minecraft/textures/block"

        for block_name in BLOCK_TEXTURES:
            block_img = generate_block_texture(block_name)
            buf = BytesIO()
            block_img.save(buf, "PNG")
            zf.writestr(f"{block_base}/{block_name}.png", buf.getvalue())

    return zip_buffer.getvalue()


def main():
    """Generate all resource pack ZIPs."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Purple Galaxy Resource Pack Generator")
    print("=" * 50)

    for version_name, pack_format in VERSION_FORMATS.items():
        zip_data = build_pack(version_name, pack_format)
        safe_name = version_name.replace(".", "_").replace("-", "_")
        filename = f"{PACK_NAME}_{safe_name}.zip"
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(zip_data)
        size_kb = len(zip_data) / 1024
        print(f"  -> {filename} ({size_kb:.1f} KB)")

    print("\nAll packs generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
