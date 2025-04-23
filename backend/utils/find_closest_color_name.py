from math import sqrt
from mycolors.xkcd_colors import xkcd_colors


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def color_distance(c1, c2):
    return sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def find_closest_color_name(target_hex, xkcd_dict):
    target_rgb = hex_to_rgb(target_hex)
    closest_name = None
    min_dist = float("inf")

    for name, hex_value in xkcd_dict.items():
        color_rgb = hex_to_rgb(hex_value)
        dist = color_distance(target_rgb, color_rgb)
        if dist < min_dist:
            min_dist = dist
            closest_name = name

    return closest_name
