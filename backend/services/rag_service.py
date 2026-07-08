import os
from dotenv import load_dotenv
from services.qdrant_service import search_jobs

load_dotenv()

try:
    from langchain_core.prompts import ChatPromptTemplate
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    ChatPromptTemplate = None


def _build_chain():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or ChatPromptTemplate is None:
        raise RuntimeError("RAG is unavailable because the required AI packages are not installed.")

    from langchain_groq import ChatGroq

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.3,
    )

    rag_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a job search assistant. Use the following job listings retrieved from the database to answer.
         If no relevant jobs are found, say clearly.
         Retrieved Jobs:
         {context}"""),
        ("human", "{question}")
    ])
    return rag_prompt | llm


def rag_job_search(question: str) -> str:
    results = search_jobs(question, top_k=5)
    if not results:
        return "No jobs found in the database. Please embed jobs first using the /rag/embed-jobs endpoint."

    context = "\n".join([
        f"-{r['title']}:{r['description']}(Salary:{r['salary']},Match:{r['score']})"
        for r in results
    ])

    try:
        chain = _build_chain()
        response = chain.invoke({"context": context, "question": question})
        return response.content
    except Exception:
        return f"[mock rag answer] {question}"