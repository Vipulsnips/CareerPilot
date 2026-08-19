"use client";

import { useState } from "react";
import type { Resume, ResumeAnalysis } from "@/types/resume";

interface ResumeUploadProps {
  onUploadSuccess: (resume: Resume, analysis: ResumeAnalysis) => void;
}

export default function ResumeUpload({ onUploadSuccess }: ResumeUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

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

      onUploadSuccess(data.resume, data.analysis);
    } catch (error) {
      console.error("Upload error:", error);
      setError("Unable to process your resume. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto mt-10 max-w-xl">
      <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="rounded-2xl border-2 border-dashed border-slate-200 bg-[#FAFBFF] px-6 py-10 transition hover:border-blue-300">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-xl">
            📄
          </div>

          <h3 className="mt-4 text-lg font-semibold">Upload your resume</h3>

          <p className="mt-2 text-sm text-slate-500">
            Upload a PDF to generate your personalized interview.
          </p>

          <label className="mt-6 inline-flex cursor-pointer rounded-xl bg-gradient-to-r from-blue-600 to-violet-600 px-6 py-3 text-sm font-semibold text-white shadow-md shadow-blue-200 transition hover:scale-[1.02]">
            {file ? "Change Resume" : "Choose Resume"}

            <input
              type="file"
              accept=".pdf"
              className="hidden"
              onChange={(event) => {
                setFile(event.target.files?.[0] ?? null);
              }}
            />
          </label>

          {file && (
            <p className="mt-4 truncate text-sm font-medium text-slate-700">
              {file.name}
            </p>
          )}

          <p className="mt-4 text-xs text-slate-400">PDF files only</p>
        </div>

        {error && <p className="mt-4 text-sm text-red-500">{error}</p>}

        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className="mt-5 w-full rounded-xl bg-[#172033] px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {loading ? "Analyzing Resume..." : "Continue →"}
        </button>
      </div>
    </div>
  );
}
