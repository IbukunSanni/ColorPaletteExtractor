from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def mood_vector(mood: str):
    return model.encode(mood)


REFERENCE_MOODS = {
    "bright": model.encode("bright"),
    "dark": model.encode("dark"),
    "warm": model.encode("warm"),
    "cool": model.encode("cool"),
    "saturated": model.encode("vibrant"),
    "desaturated": model.encode("muted"),
}


def get_adjustment_weights(mood: str):
    vec = mood_vector(mood)
    weights = {}
    for key, ref_vec in REFERENCE_MOODS.items():
        sim = np.dot(vec, ref_vec) / (np.linalg.norm(vec) * np.linalg.norm(ref_vec))
        weights[key] = sim
    return weights


def adjust_palette_by_mood(base_colors, mood):
    # Dummy variation based on mood
    if mood.lower() == "dark":
        return [shade_color(c, factor=0.6) for c in base_colors]
    elif mood.lower() == "pastel":
        return [tint_color(c, factor=0.4) for c in base_colors]
    return base_colors


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
