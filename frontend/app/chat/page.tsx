"use client";

import { useState } from "react";

type Message = {
  role: "student" | "teacher";
  content: string;
  student?: string;
  teacher_followup?: string;
  sources?: Source[];
};

type Source = {
  page: number;
  text: string;
};

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [ingesting, setIngesting] = useState(false);
  const [ingestStatus, setIngestStatus] = useState<string | null>(null);
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [uploadingPdf, setUploadingPdf] = useState(false);
  const [pdfStatus, setPdfStatus] = useState<string | null>(null);

  async function handleAsk() {
    if (!question.trim()) return;

    setLoading(true);
    setError(null);

    const studentMessage: Message = {
      role: "student",
      content: question,
    };

    setHistory((prev) => [...prev, studentMessage]);
    setQuestion("");

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          history: history.map((m) => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      if (!res.ok) {
        throw new Error("Server error");
      }

      const data = await res.json();

      const teacherMessage: Message = {
        role: "teacher",
        content: data.teacher || "",
        student: data.student,
        teacher_followup: data.teacher_followup,
        sources: data.sources || [],
      };

      setHistory((prev) => [...prev, teacherMessage]);
    } catch (err) {
      setError("Failed to get response from server");
    } finally {
      setLoading(false);
    }
  }

  async function handleIngestYoutube() {
    if (!youtubeUrl.trim()) return;

    setIngesting(true);
    setIngestStatus(null);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/ingest/youtube?url=${encodeURIComponent(
          youtubeUrl
        )}`,
        {
          method: "POST",
        }
      );

      if (!res.ok) {
        throw new Error("Failed to ingest YouTube video");
      }

      const data = await res.json();

      setIngestStatus(
        `✅ YouTube video ingested successfully (${data.chunks_added} chunks)`
      );
      setYoutubeUrl("");
    } catch (err) {
      setIngestStatus("❌ Failed to ingest YouTube video");
    } finally {
      setIngesting(false);
    }
  }

  async function handleUploadPdf() {
    if (!pdfFile) return;

    setUploadingPdf(true);
    setPdfStatus(null);

    try {
      const formData = new FormData();
      formData.append("file", pdfFile);

      const res = await fetch("http://127.0.0.1:8000/ingest/pdf", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Failed to upload PDF");
      }

      const data = await res.json();

      setPdfStatus(
        `✅ PDF "${data.pdf}" uploaded successfully (${data.chunks_added} chunks)`
      );
      setPdfFile(null);
    } catch (err) {
      setPdfStatus("❌ Failed to upload PDF");
    } finally {
      setUploadingPdf(false);
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-6 p-6">
          <h1 className="text-3xl font-semibold text-gray-900 mb-2">
            Interactive Study Tool
          </h1>
          <p className="text-gray-600 text-sm">
            Ask questions about your study materials
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6 min-h-[500px] max-h-[600px] overflow-y-auto">
          {history.length === 0 && (
            <div className="flex items-center justify-center h-full text-gray-400">
              <p>Start a conversation by asking a question below</p>
            </div>
          )}

          <div className="space-y-6">
            {history.map((msg, idx) => (
              <div key={idx}>
                {msg.role === "student" ? (
                  <div className="flex justify-end">
                    <div className="bg-blue-600 text-white rounded-2xl rounded-tr-sm px-6 py-3 max-w-[80%] shadow-sm">
                      <p className="whitespace-pre-wrap break-words">
                        {msg.content}
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 text-gray-900 rounded-2xl rounded-tl-sm px-6 py-4 max-w-[85%] shadow-sm">
                      {msg.content && (
                        <div className="mb-4">
                          <h3 className="font-semibold text-sm text-gray-700 mb-2">
                            Teacher Explanation
                          </h3>
                          <p className="whitespace-pre-wrap break-words leading-relaxed">
                            {msg.content}
                          </p>
                        </div>
                      )}

                      {msg.student && (
                        <div className="mb-4 border-t border-gray-300 pt-4">
                          <h3 className="font-semibold text-sm text-gray-700 mb-2">
                            Student Follow-up Question
                          </h3>
                          <p className="whitespace-pre-wrap break-words leading-relaxed text-gray-800">
                            {msg.student}
                          </p>
                        </div>
                      )}

                      {msg.teacher_followup && (
                        <div className="mb-4 border-t border-gray-300 pt-4">
                          <h3 className="font-semibold text-sm text-gray-700 mb-2">
                            Teacher Clarification
                          </h3>
                          <p className="whitespace-pre-wrap break-words leading-relaxed">
                            {msg.teacher_followup}
                          </p>
                        </div>
                      )}

                      {msg.sources && msg.sources.length > 0 && (
                        <div className="mt-4 border-t border-gray-300 pt-4">
                          <h3 className="font-semibold text-sm text-gray-700 mb-3">
                            Sources
                          </h3>
                          <div className="space-y-2">
                            {msg.sources.map((source, i) => (
                              <div
                                key={i}
                                className="bg-white border border-gray-200 rounded-lg p-3"
                              >
                                <div className="flex items-start gap-2">
                                  <span className="inline-flex items-center justify-center bg-blue-100 text-blue-700 text-xs font-semibold px-2 py-1 rounded">
                                    Page {source.page}
                                  </span>
                                  <p className="text-sm text-gray-700 leading-relaxed flex-1">
                                    {source.text.slice(0, 120)}
                                    {source.text.length > 120 ? "..." : ""}
                                  </p>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-700 rounded-2xl rounded-tl-sm px-6 py-4 max-w-[85%] shadow-sm">
                  <div className="flex items-center gap-2">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                    </div>
                    <span className="text-sm">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-6">
            <p className="text-sm">{error}</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Upload PDF
            </h2>
            
            <input
              type="file"
              accept=".pdf"
              className="w-full border border-gray-300 rounded-lg px-4 py-3 mb-3 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
              onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) setPdfFile(file);
              }}
              disabled={uploadingPdf}
            />

            {pdfFile && (
              <p className="text-sm text-gray-600 mb-3">
                Selected: {pdfFile.name}
              </p>
            )}

            <button
              onClick={handleUploadPdf}
              disabled={uploadingPdf || !pdfFile}
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors w-full"
            >
              {uploadingPdf ? "Uploading..." : "Upload PDF"}
            </button>

            {pdfStatus && (
              <p className="mt-3 text-sm font-medium">{pdfStatus}</p>
            )}
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Add YouTube Video
            </h2>
            
            <input
              type="text"
              className="w-full border border-gray-300 rounded-lg px-4 py-3 mb-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Paste YouTube URL here..."
              value={youtubeUrl}
            onChange={(e) => setYoutubeUrl(e.target.value)}
            disabled={ingesting}
          />

          <button
            onClick={handleIngestYoutube}
            disabled={ingesting || !youtubeUrl.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors w-full"
          >
            {ingesting ? "Ingesting..." : "Ingest Video"}
          </button>

          {ingestStatus && (
            <p className="mt-3 text-sm font-medium">{ingestStatus}</p>
          )}
        </div>
      </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <div className="flex gap-3">
            <textarea
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={3}
              placeholder="Ask a question about your study materials..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleAsk();
                }
              }}
              disabled={loading}
            />
            <button
              onClick={handleAsk}
              disabled={loading || !question.trim()}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors self-end"
            >
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Press Enter to send, Shift+Enter for new line
          </p>
        </div>
      </div>
    </main>
  );
}
