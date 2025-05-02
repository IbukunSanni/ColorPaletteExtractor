from colorthief import ColorThief
from io import BytesIO


def extract_colors(buffer):
    ct = ColorThief(buffer)
    palette = ct.get_palette(color_count=5)
    return [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in palette]
