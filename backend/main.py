from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from utils.color_extractor import extract_colors
from utils.mood_adjuster import adjust_palette_by_mood
from utils.png_exporter import generate_png_swatch
from utils.find_closest_color_name import find_closest_color_name

from fastapi.responses import JSONResponse, StreamingResponse
from io import BytesIO
from mycolors.xkcd_colors import xkcd_colors
from PIL import Image


app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://color-palette-extractor.vercel.app/",
    ],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "✅ FastAPI backend is running!"}


@app.post("/")
def post_root():
    return {"message": "✅ POST received! FastAPI is working."}


@app.post("/extract-colors")
async def extract_colors_endpoint(file: UploadFile = File(...)):
    image_bytes = await file.read()

    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = image.resize((100, 100))  # downscale to reduce memory
    colors = extract_colors(image_bytes)

    names = [find_closest_color_name(color, xkcd_colors) for color in colors]
    return {"colors": colors, "names": names}


@app.post("/adjust-mood")
async def adjust_mood_endpoint(
    mood: str = Form(...), base_colors: list[str] = Form(...)
):
    palette = adjust_palette_by_mood(base_colors, mood)
    names = [find_closest_color_name(color, xkcd_colors) for color in palette]
    return {"adjusted_colors": palette, "names": names}


@app.post("/export-png")
async def export_png(colors: list[str] = Form(...)):
    image = generate_png_swatch(colors)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")
