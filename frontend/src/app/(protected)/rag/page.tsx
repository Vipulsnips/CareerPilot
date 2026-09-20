"use client";

import { useState } from "react";
import { useAuth } from "@clerk/nextjs";

export default function RagPage() {
  const { getToken } = useAuth();

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askQuestion() {
    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setAnswer("");
    setError("");

    try {
      const token = await getToken();

      if (!token) {
        throw new Error("Unable to authenticate user");
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/rag/ask`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            question,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to get answer");
      }

      const data = await response.json();

      setAnswer(data.answer);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>Resume RAG</h1>

      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something about your resume..."
      />

      <button onClick={askQuestion} disabled={loading}>
        {loading ? "Asking..." : "Ask"}
      </button>

      {error && <p>{error}</p>}

      {answer && (
        <div>
          <h2>Answer</h2>
          <p>{answer}</p>
        </div>
      )}
    </main>
  );
}