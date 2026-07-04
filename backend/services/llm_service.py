import os

try:
    import openai  # type: ignore
except ImportError:
    openai = None


def llm_response(prompt: str) -> str:
    """Return a simple LLM reply or a mock reply when OpenAI is unavailable."""
    if openai and (os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")):
        response = openai.ChatCompletion.create(
            model=os.getenv("OPENAI_CHAT_MODEL", "gpt-3.5-turbo"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    return f"[mock llm reply] {prompt}"
