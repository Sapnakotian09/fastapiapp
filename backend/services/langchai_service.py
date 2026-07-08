import os
from typing import Any

try:
    from dotenv import load_dotenv
    from langchain_groq import ChatGroq
    from langchain.core.prompts import ChatPromptTemplate
    from langchain_core.runnable import RunnableWithMessageHistory
    from langchain_community.chat_message_histories import ChatMessageHistory

    load_dotenv()
    llm = ChatGroq(
        model=os.getenv("LLAMA_MODEL", "llama-3.3-70b-versatile"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.5,
    )
    prompt_with_memory = ChatPromptTemplate.from_messages([
        ("system", "you are a helpful career guidance assistant"),
        ("placeholder", "{chat_history}"),
        ("human", "{user_query}"),
    ])
    chain_with_memory = prompt_with_memory | llm
    store: dict[str, ChatMessageHistory] = {}

    def get_history(session_id: str) -> ChatMessageHistory:
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    chat_with_memory = RunnableWithMessageHistory(
        runnable=chain_with_memory,
        get_message_history=get_history,
        input_messages_key="user_query",
        history_messages_key="chat_history",
    )

    def ask_career_chatbot_response(question: str, session_id: str = "default") -> str:
        response = chat_with_memory.invoke(
            {"user_query": question}, {"configurable": {"session_id": session_id}}
        )
        return getattr(response, "content", str(response))

except ModuleNotFoundError:
    try:
        from services.llm_service import llm_response

        def ask_career_chatbot_response(question: str, session_id: str = "default") -> str:
            # Fallback to the simple LLM service (OpenAI) if available
            try:
                return llm_response(question)
            except Exception:
                return f"[mock career reply] {question}"
    except Exception:
        def ask_career_chatbot_response(question: str, session_id: str = "default") -> str:
            # Simple rule-based fallback to provide useful career guidance
            q = (question or "").strip().lower()
            if not q:
                return "Hi — what would you like to learn or ask about your career?"

            # Learning intent
            if any(k in q for k in ["learn", "learning", "want to learn", "how to learn"]):
                return (
                    "Great — tell me the specific skill or topic you want to learn. "
                    "A good plan: 1) Define a clear goal, 2) Learn fundamentals from a beginner course or book, "
                    "3) Build small projects, 4) Practice consistently and track progress. "
                    "I can suggest resources if you tell me the topic (e.g., Python, React, data science)."
                )

            # Career path / job search intent
            if any(k in q for k in ["job", "apply", "interview", "career", "hire"]):
                return (
                    "For job search: clarify your target role, tailor your resume to match job descriptions, "
                    "practice common interview questions, prepare a small portfolio project, and network on LinkedIn. "
                    "Tell me your target role and experience level and I can give a step-by-step plan."
                )

            # Skill improvement intent
            if any(k in q for k in ["improve", "practice", "project", "portfolio"]):
                return (
                    "To improve skills, pick focused projects, get feedback (code review or mentor), "
                    "and iterate. Break projects into weekly milestones and measure outcomes."
                )

            # Default helpful response
            return (
                "Thanks — I can help with learning plans, job search advice, and project ideas. "
                "Please rephrase with more detail (topic, experience, or goal) so I can give actionable steps."
            )

except Exception as exc:
    def ask_career_chatbot_response(question: str, session_id: str = "default") -> str:
        return f"[career service unavailable] {exc}"
