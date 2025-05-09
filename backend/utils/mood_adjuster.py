from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import colorsys

# 🔧 Load model once at startup (not per request)
print("🧠 Loading transformer model...")
# model = SentenceTransformer("paraphrase-albert-small-v2")
print("✅ Model loaded.")


# 🎨 COLOR HELPERS
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


# 🧠 MOOD ENCODING
def mood_vector(mood: str):
    return model.encode(mood)


REFERENCE_ENCODINGS = {
    label: model.encode(label)
    for label in ["bright", "dark", "warm", "cool", "vibrant", "muted"]
}


def get_adjustment_weights(mood: str):
    vec = model.encode(mood)
    weights = {}
    for key, ref_vec in REFERENCE_ENCODINGS.items():
        sim = np.dot(vec, ref_vec) / (np.linalg.norm(vec) * np.linalg.norm(ref_vec))
        weights[key] = sim
    return weights


# 🎯 MAIN ADJUSTMENT FUNCTION
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

        # Warm/cool hue shift
        shift = (
            0.03 * weights["warm"]
            if weights["warm"] > weights["cool"]
            else -0.03 * weights["cool"]
        )
        r, g, b = adjust_hue(r, g, b, shift)

        # Saturation tweak
        if weights["saturated"] > weights["desaturated"]:
            sat_factor = 1 + (weights["saturated"] - weights["desaturated"]) * 0.5
        else:
            sat_factor = 1 - (weights["desaturated"] - weights["saturated"]) * 0.5
        r, g, b = adjust_saturation(r, g, b, sat_factor)

        return rgb_to_hex(r, g, b)

    print(f"🎨 Mood Weights: {weights}")
    return [adjust_color(c) for c in base_colors]
