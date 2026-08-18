"use client";

import { useState } from "react";
import type { Resume, ResumeAnalysis } from "@/types/resume";

interface InterviewConfigProps {
  resume: Resume;
  analysis: ResumeAnalysis;
}

export default function InterviewConfig({
  resume,
  analysis,
}: InterviewConfigProps) {
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [questionCount, setQuestionCount] = useState(5);

  const toggleSkill = (skill: string) => {
    setSelectedSkills((current) =>
      current.includes(skill)
        ? current.filter((item) => item !== skill)
        : [...current, skill],
    );
  };

  return (
    <div className="mx-auto mt-10 max-w-xl rounded-3xl border border-slate-200 bg-white p-8 text-left shadow-sm">
      <div>
        <p className="text-sm font-semibold text-blue-600">RESUME ANALYZED</p>

        <h3 className="mt-2 text-2xl font-bold">Welcome, {resume.name}</h3>

        <p className="mt-2 text-sm text-slate-500">
          Choose what you want to focus on in your interview.
        </p>
      </div>

      <div className="mt-8">
        <h4 className="text-sm font-semibold text-slate-700">Select skills</h4>

        <div className="mt-3 flex flex-wrap gap-2">
          {[...new Set(resume.skills)].map((skill) => (
            <button
              key={skill}
              type="button"
              onClick={() => toggleSkill(skill)}
              className={`rounded-full px-4 py-2 text-sm font-medium transition ${
                selectedSkills.includes(skill)
                  ? "bg-blue-600 text-white"
                  : "bg-slate-100 text-slate-700 hover:bg-slate-200"
              }`}
            >
              {skill}
            </button>
          ))}
        </div>
      </div>

      <div className="mt-8">
        <h4 className="text-sm font-semibold text-slate-700">
          Number of questions
        </h4>

        <div className="mt-3 flex items-center gap-3">
          <button
            type="button"
            onClick={() =>
              setQuestionCount((current) => Math.max(1, current - 1))
            }
            disabled={questionCount === 1}
            className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-lg font-semibold text-slate-700 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
          >
            −
          </button>

          <div className="flex h-10 min-w-16 items-center justify-center rounded-xl border border-slate-200 bg-white px-4 text-sm font-semibold text-slate-800">
            {questionCount}
          </div>

          <button
            type="button"
            onClick={() =>
              setQuestionCount((current) => Math.min(20, current + 1))
            }
            disabled={questionCount === 20}
            className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-lg font-semibold text-slate-700 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-40"
          >
            +
          </button>
        </div>

        <p className="mt-2 text-xs text-slate-400">
          Choose between 1 and 20 questions.
        </p>
      </div>

      <div className="mt-8 rounded-2xl bg-[#FAFBFF] p-4">
        <p className="text-sm font-semibold text-slate-700">Your strengths</p>

        <p className="mt-2 text-sm text-slate-500">
          {analysis.strengths.length} strengths identified from your resume.
        </p>
      </div>

      <button
        type="button"
        disabled={selectedSkills.length === 0}
        className="mt-6 w-full rounded-xl bg-[#172033] px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
      >
        Start Interview →
      </button>
    </div>
  );
}
