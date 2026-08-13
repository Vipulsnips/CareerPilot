"use client";

import { useState } from "react";

export default function ResumeUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:8000/resume/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload resume");
      }

      const data = await response.json();

      console.log("Resume response:", data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-8">
      <input
        type="file"
        accept=".pdf"
        onChange={(event) => {
          setFile(event.target.files?.[0] ?? null);
        }}
        className="block w-full text-sm text-slate-400"
      />

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="mt-6 rounded-lg bg-blue-600 px-6 py-3 font-medium disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Analyzing Resume..." : "Upload Resume"}
      </button>
    </div>
  );
}