import { useState } from "react";
import api from "../Services/api";
import type { ChatRequest, ChatResponse } from "../types/chat";

function ChatPage() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    setError("");
    setResponse("");

    const payload: ChatRequest = {
      message: message.trim(),
      session_id: "default",
    };

    try {
      const result = await api.post<ChatResponse>("/chat/ask career", payload);
      setResponse(result.data.response);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err.message || "Failed to get a response.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="page-section chat-page">
      <div className="page-header">
        <h1>Career Chat</h1>
        <p>Ask about career advice and receive a quick response.</p>
      </div>

      <form className="chat-form" onSubmit={handleSubmit}>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          rows={6}
          placeholder="Type your career question here..."
        />
        <button type="submit" disabled={loading || !message.trim()}>
          {loading ? "Sending..." : "Send"}
        </button>
      </form>

      {error && <div className="page-error">{error}</div>}

      {response && (
        <div className="chat-response">
          <strong>Response</strong>
          <p>{response}</p>
        </div>
      )}
    </section>
  );
}

export default ChatPage;