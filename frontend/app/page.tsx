"use client";
import Layout from "@/components/Layout";
import ImageUploader from "@/components/ImageUploader";
import MoodInput from "@/components/MoodInput";
import { useState, useEffect } from "react";

export default function Home() {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [mood, setMood] = useState("");
  const [palette, setPalette] = useState([]);
  const [colorNames, setColorNames] = useState([]);
  const [newPalette, setNewPalette] = useState([]);

  const handleAdjustMood = async () => {
    if (palette.length === 0 || !mood) return;

    console.log("palette prior to adjust:", palette);
    console.log("mood prior to adjust:", mood);

    const formData = new FormData();
    formData.append("mood", mood);
    palette.forEach((color, i) => {
      formData.append("base_colors", color); // backend expects a list of HEX strings
    });

    // TODO: remove console.log
    formData.forEach((value, key) => {
      console.log(`${key}: ${value}`);
    });

    try {
      const res = await fetch("http://localhost:8000/adjust-mood", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setNewPalette(data.adjusted_colors);
    } catch (err) {
      console.error("Mood adjust failed:", err);
    }
  };

  useEffect(() => {
    // console.log("palette changed:", palette);
    // console.log("names changed:", colorNames);
  }, [palette, colorNames]);

  return (
    <Layout>
      <ImageUploader
        // onImageUpload={(file) => setImageFile(file)}
        onColorExtracted={(colors) => setPalette(colors)}
        onColorNamesExtracted={(names) => setColorNames(names)}
      />
      {palette.length > 0 && (
        <div className="mt-4">
          <p className="text-sm text-gray-600">
            <strong>Extracted Colors:</strong>
          </p>
          <div className="flex space-x-4 mt-2 flex-wrap">
            {palette.map((color, index) => (
              <div key={index} className="flex flex-col items-center">
                <div
                  className="w-8 h-8 rounded mb-1"
                  style={{ backgroundColor: color }}
                  title={color}
                ></div>
                <span className="text-xs text-center text-gray-700">
                  {colorNames?.[index] || "Unnamed"}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      <MoodInput onMoodChange={(m) => setMood(m)} />

      <button
        onClick={handleAdjustMood}
        className="mt-4 bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700 transition"
      >
        Adjust Colors by Mood
      </button>

      {newPalette.length > 0 && (
        <div className="mt-4">
          <p className="text-sm text-gray-600">
            <strong>Adjusted Colors:</strong>
          </p>
          <div className="flex space-x-2 mt-2">
            {newPalette.map((color, index) => (
              <div key={index} className="flex flex-col items-center">
                <div
                  className="w-8 h-8 rounded"
                  style={{ backgroundColor: color }}
                  title={color}
                ></div>
                <div className="text-sm text-center mt-1">
                  {colorNames[index]}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-4 text-sm text-gray-600">
        <p>
          <strong>Image:</strong> {imageFile?.name || "No image selected"}
        </p>
        <p>
          <strong>Mood:</strong> {mood || "No mood entered"}
        </p>
      </div>
    </Layout>
  );
}
