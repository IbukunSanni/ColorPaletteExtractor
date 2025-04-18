from PIL import Image, ImageDraw


def generate_png_swatch(colors):
    width = 100 * len(colors)
    height = 100
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    for i, color in enumerate(colors):
        draw.rectangle([i * 100, 0, (i + 1) * 100, height], fill=color)
    return image
