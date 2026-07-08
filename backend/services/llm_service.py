import os

try:
    import openai  # type: ignore
except ImportError:
    openai = None


def llm_response(prompt: str) -> str:
    """Return an LLM reply or a helpful fallback when OpenAI is unavailable."""
    if openai and os.getenv("OPENAI_API_KEY"):
        response = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    # Helpful fallback when OpenAI is not configured
    message = (prompt or "").strip().lower()
    if not message:
        return "Hi! What would you like to know? Ask me about learning, career advice, or skills."

    if any(k in message for k in ["learn", "learning", "study", "how to"]):
        return (
            "To learn effectively, start with one focused topic, follow a beginner-friendly course, "
            "practice by building small projects, and review your work regularly. Tell me what you want to learn and I can give a step-by-step plan."
        )

    if any(k in message for k in ["job", "career", "interview", "work", "apply"]):
        return (
            "For career growth, clarify your target role, tailor your resume to the job description, "
            "practice common interview questions, build a small portfolio, and network with professionals in your field. "
            "Tell me your current skills and goals for more specific advice."
        )

    if any(k in message for k in ["react", "node", "python", "java", "sql", "frontend", "backend"]):
        return (
            "Your skills are a great start. Focus on one technology at a time, build practical projects, "
            "and learn how to explain your experience clearly. Ask me for a project idea or study path."
        )

    return (
        "I can help with learning plans, job search advice, and career steps. "
        "Please ask a specific question like 'How do I learn React?' or 'How can I prepare for a software developer interview?'"
    )
