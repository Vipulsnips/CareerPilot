"use client";

import { useState } from "react";
import type { Resume } from "@/types/resume";
import type { InterviewQuestions } from "@/types/interview";
import { useAuth } from "@clerk/nextjs";

interface AnswerEvaluation {
  score: number;
  strengths: string[];
  weaknesses: string[];
  feedback: string;
}

interface RagResponse {
  answer: string;
}

interface InterviewScreenProps {
  resume: Resume;
  questions: InterviewQuestions;
}

export default function InterviewScreen({
  resume,
  questions,
}: InterviewScreenProps) {
  const { getToken } = useAuth();

  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState<AnswerEvaluation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [showResumeAssistant, setShowResumeAssistant] = useState(false);
  const [resumeQuestion, setResumeQuestion] = useState("");
  const [resumeAnswer, setResumeAnswer] = useState("");
  const [resumeLoading, setResumeLoading] = useState(false);
  const [resumeError, setResumeError] = useState<string | null>(null);

  const currentQuestion = questions.questions[currentIndex];

  if (!currentQuestion) {
    return null;
  }

  const handleSubmitAnswer = async () => {
    if (!answer.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const token = await getToken();

      if (!token) {
        throw new Error("Unable to authenticate user");
      }

      const API_URL = process.env.NEXT_PUBLIC_API_URL;

      const response = await fetch(`${API_URL}/interview/evaluate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          resume,
          question: currentQuestion,
          answer,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to evaluate answer");
      }

      const data: AnswerEvaluation = await response.json();

      setEvaluation(data);
    } catch (error) {
      console.error("Answer evaluation error:", error);
      setError("Unable to evaluate your answer. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleAskResume = async () => {
    if (!resumeQuestion.trim()) return;

    setResumeLoading(true);
    setResumeError(null);
    setResumeAnswer("");

    try {
      const token = await getToken();

      if (!token) {
        throw new Error("Unable to authenticate user");
      }

      const API_URL = process.env.NEXT_PUBLIC_API_URL;

      const response = await fetch(`${API_URL}/rag/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          question: resumeQuestion,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get answer");
      }

      const data: RagResponse = await response.json();

      setResumeAnswer(data.answer);
    } catch (error) {
      console.error("Resume assistant error:", error);
      setResumeError("Unable to answer your question. Please try again.");
    } finally {
      setResumeLoading(false);
    }
  };

  const handleNextQuestion = () => {
    setCurrentIndex((current) => current + 1);
    setAnswer("");
    setEvaluation(null);
    setError(null);

    setResumeQuestion("");
    setResumeAnswer("");
    setResumeError(null);
    setShowResumeAssistant(false);
  };

  const isLastQuestion = currentIndex === questions.questions.length - 1;

  return (
    <div className="mx-auto mt-10 max-w-3xl rounded-3xl border border-slate-200 bg-white p-8 text-left shadow-sm">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold text-blue-600">AI INTERVIEW</p>

          <h3 className="mt-1 text-xl font-bold">Welcome, {resume.name}</h3>
        </div>

        <p className="text-sm font-medium text-slate-500">
          Question {currentIndex + 1} / {questions.questions.length}
        </p>
      </div>

      {/* Progress */}
      <div className="mt-5 h-2 overflow-hidden rounded-full bg-slate-100">
        <div
          className="h-full rounded-full bg-gradient-to-r from-blue-600 to-violet-600 transition-all"
          style={{
            width: `${
              ((currentIndex + 1) / questions.questions.length) * 100
            }%`,
          }}
        />
      </div>

      {/* Question */}
      <div className="mt-8">
        <div className="flex gap-2">
          <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-600">
            {currentQuestion.category}
          </span>

          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
            {currentQuestion.difficulty}
          </span>
        </div>

        <h2 className="mt-5 text-2xl font-bold leading-9 text-slate-800">
          {currentQuestion.question}
        </h2>
      </div>

      {/* Ask Your Resume */}
      <div className="mt-8 rounded-2xl border border-blue-100 bg-blue-50/50">
        <button
          type="button"
          onClick={() => setShowResumeAssistant((current) => !current)}
          className="flex w-full items-center justify-between px-5 py-4 text-left"
        >
          <div>
            <p className="text-sm font-semibold text-slate-800">
              📄 Ask Your Resume
            </p>

            <p className="mt-1 text-xs text-slate-500">
              Need a reminder about your experience or projects?
            </p>
          </div>

          <span className="text-sm font-semibold text-blue-600">
            {showResumeAssistant ? "Hide" : "Ask"}
          </span>
        </button>

        {showResumeAssistant && (
          <div className="border-t border-blue-100 px-5 pb-5 pt-4">
            <textarea
              value={resumeQuestion}
              onChange={(event) => setResumeQuestion(event.target.value)}
              placeholder="e.g. What did I use Redis for?"
              rows={3}
              disabled={resumeLoading}
              className="w-full resize-none rounded-xl border border-slate-200 bg-white p-3 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 disabled:opacity-60"
            />

            <button
              type="button"
              onClick={handleAskResume}
              disabled={!resumeQuestion.trim() || resumeLoading}
              className="mt-3 rounded-xl bg-blue-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {resumeLoading ? "Thinking..." : "Ask Resume →"}
            </button>

            {resumeError && (
              <p className="mt-3 text-sm text-red-500">{resumeError}</p>
            )}

            {resumeAnswer && (
              <div className="mt-4 rounded-xl bg-white p-4">
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                  Answer
                </p>

                <p className="mt-2 text-sm leading-6 text-slate-600">
                  {resumeAnswer}
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Answer */}
      {!evaluation && (
        <>
          <div className="mt-8">
            <label className="text-sm font-semibold text-slate-700">
              Your answer
            </label>

            <textarea
              value={answer}
              onChange={(event) => setAnswer(event.target.value)}
              placeholder="Type your answer here..."
              rows={7}
              disabled={loading}
              className="mt-3 w-full resize-none rounded-2xl border border-slate-200 bg-[#FAFBFF] p-4 text-sm text-slate-700 outline-none transition placeholder:text-slate-400 focus:border-blue-400 focus:ring-2 focus:ring-blue-100 disabled:opacity-60"
            />
          </div>

          {error && <p className="mt-4 text-sm text-red-500">{error}</p>}

          <button
            type="button"
            onClick={handleSubmitAnswer}
            disabled={!answer.trim() || loading}
            className="mt-5 w-full rounded-xl bg-[#172033] px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
          >
            {loading ? "Evaluating Answer..." : "Submit Answer →"}
          </button>
        </>
      )}

      {/* Evaluation */}
      {evaluation && (
        <div className="mt-8">
          <div className="rounded-2xl bg-[#FAFBFF] p-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-slate-800">AI Feedback</h3>

              <div className="rounded-xl bg-blue-50 px-4 py-2 text-sm font-bold text-blue-600">
                Score: {evaluation.score}/10
              </div>
            </div>

            <div className="mt-6">
              <h4 className="text-sm font-semibold text-slate-700">
                Strengths
              </h4>

              <ul className="mt-2 space-y-1">
                {evaluation.strengths.map((strength, index) => (
                  <li key={index} className="text-sm text-slate-500">
                    • {strength}
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-5">
              <h4 className="text-sm font-semibold text-slate-700">
                Areas to improve
              </h4>

              <ul className="mt-2 space-y-1">
                {evaluation.weaknesses.map((weakness, index) => (
                  <li key={index} className="text-sm text-slate-500">
                    • {weakness}
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-5">
              <h4 className="text-sm font-semibold text-slate-700">Feedback</h4>

              <p className="mt-2 text-sm leading-6 text-slate-500">
                {evaluation.feedback}
              </p>
            </div>
          </div>

          <button
            type="button"
            onClick={handleNextQuestion}
            className="mt-5 w-full rounded-xl bg-[#172033] px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            {isLastQuestion ? "Finish Interview" : "Next Question →"}
          </button>
        </div>
      )}
    </div>
  );
}