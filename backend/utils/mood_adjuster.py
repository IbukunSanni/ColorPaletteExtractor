from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from functools import lru_cache
import colorsys


def hex_to_rgb(hex_color):
    r = int(hex_color[1:3], 16) / 255.0
    g = int(hex_color[3:5], 16) / 255.0
    b = int(hex_color[5:7], 16) / 255.0
    return r, g, b


def rgb_to_hex(r, g, b):
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def adjust_hue(r, g, b, shift):
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + shift) % 1.0
    return colorsys.hls_to_rgb(h, l, s)


def adjust_saturation(r, g, b, factor):
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    s = max(0.0, min(1.0, s * factor))
    return colorsys.hls_to_rgb(h, l, s)


@lru_cache()
def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def mood_vector(mood: str):
    model = get_model()
    return model.encode(mood)


def get_adjustment_weights(mood: str):
    vec = mood_vector(mood)
    model = get_model()
    weights = {}
    reference_moods = {
        "bright": model.encode("bright"),
        "dark": model.encode("dark"),
        "warm": model.encode("warm"),
        "cool": model.encode("cool"),
        "saturated": model.encode("vibrant"),
        "desaturated": model.encode("muted"),
    }

    for key, ref_vec in reference_moods.items():
        sim = np.dot(vec, ref_vec) / (np.linalg.norm(vec) * np.linalg.norm(ref_vec))
        weights[key] = sim
    return weights


def shade_color(hex_color, factor=0.7):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def tint_color(hex_color, factor=0.4):
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def adjust_palette_by_mood(base_colors, mood):
    weights = get_adjustment_weights(mood)

    def adjust_color(hex_color):
        r, g, b = hex_to_rgb(hex_color)

        # Darken
        if weights["dark"] > 0.5:
            factor = 1 - weights["dark"] * 0.4
            r *= factor
            g *= factor
            b *= factor

        # Brighten
        if weights["bright"] > 0.5:
            factor = weights["bright"] * 0.4
            r += (1 - r) * factor
            g += (1 - g) * factor
            b += (1 - b) * factor

        # Hue shift (warm vs cool)
        if weights["warm"] > weights["cool"]:
            shift = 0.03 * weights["warm"]  # red/yellow shift
        else:
            shift = -0.03 * weights["cool"]  # blue shift
        r, g, b = adjust_hue(r, g, b, shift)

        # Saturation adjust
        if weights["saturated"] > weights["desaturated"]:
            sat_factor = 1 + (weights["saturated"] - weights["desaturated"]) * 0.5
        else:
            sat_factor = 1 - (weights["desaturated"] - weights["saturated"]) * 0.5
        r, g, b = adjust_saturation(r, g, b, sat_factor)

        return rgb_to_hex(r, g, b)

    print("adjusted palette's done")
    print(f"weights: {weights}")
    return [adjust_color(c) for c in base_colors]
