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
    def ask_career_chatbot_response(question: str, session_id: str = "default") -> str:
        return f"[mock career reply] {question}"

except Exception as exc:
    def ask_career_chatbot_response(question: str, session_id: str = "default") -> str:
        return f"[career service unavailable] {exc}"
