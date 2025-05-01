"use client";

import { useState, useEffect } from "react";
import Layout from "@/components/Layout";
import ImageUploader from "@/components/ImageUploader";
import MoodInput from "@/components/MoodInput";
import { API_BASE_URL } from "@/lib/constants";

export default function Home() {
  // const [imageFile, setImageFile] = useState<File | null>(null);
  const [mood, setMood] = useState<string>("");
  const [palette, setPalette] = useState<string[]>([]);
  const [colorNames, setColorNames] = useState<string[]>([]);
  const [newPalette, setNewPalette] = useState<string[]>([]);
  const [newColorNames, setNewColorNames] = useState<string[]>([]);

  const handleAdjustMood = async () => {
    if (palette.length === 0 || !mood) return;

    const formData = new FormData();
    formData.append("mood", mood);
    palette.forEach((color) => {
      formData.append("base_colors", color);
    });

    try {
      const res = await fetch(`${API_BASE_URL}/adjust-mood`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setNewPalette(data.adjusted_colors);
      setNewColorNames(data.names);
    } catch (err) {
      console.error("Mood adjust failed:", err);
    }
  };

  useEffect(() => {
    // for debugging
    // console.log("palette changed:", palette);
    // console.log("names changed:", colorNames);
  }, [palette, colorNames]);

  return (
    <Layout>
      <ImageUploader
        // onImageUpload={(file: File) => setImageFile(file)}
        onColorExtracted={(colors: string[]) => setPalette(colors)}
        onColorNamesExtracted={(names: string[]) => setColorNames(names)}
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

      <MoodInput onMoodChange={(m: string) => setMood(m)} />

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
                  {newColorNames[index]}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-4 text-sm text-gray-600">
        <p>
          {/* <strong>Image:</strong> {imageFile?.name || "No image selected"} */}
        </p>
        <p>
          <strong>Mood:</strong> {mood || "No mood entered"}
        </p>
      </div>
    </Layout>
  );
}
