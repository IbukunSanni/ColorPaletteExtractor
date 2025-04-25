"use client";

import Image from "next/image";
import { useState } from "react";

type ImageUploaderProps = {
  onColorExtracted: (colors: string[]) => void;
  onColorNamesExtracted: (names: string[]) => void;
};

export default function ImageUploader({
  onColorExtracted,
  onColorNamesExtracted,
}: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/extract-colors", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      onColorNamesExtracted(data.names);
      onColorExtracted(data.colors);
    } catch (err) {
      console.error("Error uploading image:", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mb-6">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Upload Image
      </label>
      <input
        id="file-input"
        type="file"
        accept="image/*"
        onChange={handleChange}
        className="hidden"
      />

      <label
        htmlFor="file-input"
        className="inline-block cursor-pointer px-4 py-2 bg-blue-600 text-white rounded-md shadow hover:bg-blue-700 transition"
      >
        Choose Image
      </label>

      {loading && (
        <p className="mt-2 text-sm text-gray-500">Extracting colors...</p>
      )}
      {preview && (
        <div className="mt-4 w-full max-w-xs">
          <Image
            src={preview}
            alt="Preview"
            width={300} // You must specify width and height
            height={300}
            className="rounded-lg shadow w-full h-auto"
          />
        </div>
      )}
    </div>
  );
}
