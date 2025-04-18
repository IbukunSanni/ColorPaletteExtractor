from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from utils.color_extractor import extract_colors
from utils.mood_adjuster import adjust_palette_by_mood
from utils.png_exporter import generate_png_swatch
from fastapi.responses import JSONResponse, StreamingResponse
from io import BytesIO

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/extract-colors")
async def extract_colors_endpoint(file: UploadFile = File(...)):
    image_bytes = await file.read()
    colors = extract_colors(image_bytes)
    return {"colors": colors}


@app.post("/adjust-mood")
async def adjust_mood_endpoint(
    mood: str = Form(...), base_colors: list[str] = Form(...)
):
    palette = adjust_palette_by_mood(base_colors, mood)
    return {"adjusted_colors": palette}


@app.post("/export-png")
async def export_png(colors: list[str] = Form(...)):
    image = generate_png_swatch(colors)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")
