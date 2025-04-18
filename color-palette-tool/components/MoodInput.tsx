"use client";
import { useState } from "react";

export default function MoodInput({ onMoodChange }: { onMoodChange: (mood: string) => void }) {
  const [mood, setMood] = useState("");
  

  return (
    <div className="mb-6">
      <label className="block text-sm font-medium text-gray-700 mb-2">Describe a Mood</label>
      <input
        type="text"
        value={mood}
        onChange={(e) => {
          setMood(e.target.value);
          onMoodChange(e.target.value);
        }}
        className="w-full border border-gray-300 rounded-md p-2"
        placeholder="e.g. calm, energetic, romantic..."
      />
    </div>
  );
}
