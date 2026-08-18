"use client";

import { useState } from "react";
import ResumeUpload from "@/components/ResumeUpload";
import type { Resume, ResumeAnalysis } from "@/types/resume";
import InterviewConfig from "@/components/InterviewConfig";

export default function Home() {
  const [resume, setResume] = useState<Resume | null>(null);
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null);

  const handleUploadSuccess = (
    uploadedResume: Resume,
    uploadedAnalysis: ResumeAnalysis,
  ) => {
    setResume(uploadedResume);
    setAnalysis(uploadedAnalysis);
  };

  return (
    <main className="min-h-screen bg-[#F6F7FB] text-[#172033]">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-6 lg:px-10">
        <header className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-blue-600 to-violet-600 text-sm font-bold text-white">
              C
            </div>

            <div>
              <h1 className="text-lg font-bold">CareerPilot</h1>
              <p className="text-xs text-slate-500">AI Interview Platform</p>
            </div>
          </div>

          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-white text-sm font-semibold shadow-sm ring-1 ring-slate-200">
            V
          </div>
        </header>

        <section className="flex flex-1 items-center justify-center py-16">
          <div className="w-full max-w-3xl text-center">
            <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-violet-600 text-xl text-white shadow-lg shadow-blue-200">
              ✦
            </div>

            <p className="mb-3 text-sm font-semibold text-blue-600">
              PERSONALIZED INTERVIEW PREPARATION
            </p>

            <h2 className="text-4xl font-bold tracking-tight sm:text-5xl">
              Master your next interview
            </h2>

            <p className="mx-auto mt-5 max-w-2xl text-base leading-7 text-slate-500">
              Upload your resume and let CareerPilot create an AI-powered
              interview tailored to your skills, projects, and experience.
            </p>

            <ResumeUpload onUploadSuccess={handleUploadSuccess} />

            {resume && analysis && (
              <InterviewConfig resume={resume} analysis={analysis} />
            )}
          </div>
        </section>

        <footer className="pb-4 text-center text-xs text-slate-400">
          Built for smarter interview preparation
        </footer>
      </div>
    </main>
  );
}
