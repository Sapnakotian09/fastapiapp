import os
from dotenv import load_dotenv

load_dotenv()


try:
    from langchain_core.prompts import ChatPromptTemplate
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    ChatPromptTemplate = None


def _build_chain():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or ChatPromptTemplate is None:
        raise RuntimeError("Resume analysis is unavailable because the required AI packages are not installed.")

    from langchain_groq import ChatGroq

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.3,
    )

    resume_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a professional resume analyser.

Analyse the given resume text and provide:

1. Key Skills found
2. Experience Level (Junior/Mid/Senior)
3. Strengths
4. Areas to Improve
5. Suggested Job Roles

Keep the analysis short and structured."""),
        ("human", "{resume_text}")
    ])
    return resume_prompt | llm


def _heuristic_resume_analysis(resume_text: str) -> str:
    text = resume_text.strip()
    lower = text.lower()
    skills_keywords = [
        "react", "node.js", "node", "javascript", "typescript", "python",
        "sql", "postgresql", "django", "flask", "api", "docker", "git",
        "cloud", "aws", "azure", "gcp", "html", "css", "rest", "graphql"
    ]
    skills_found = sorted({kw for kw in skills_keywords if kw in lower})

    experience_level = "Entry level"
    if any(x in lower for x in ["senior", "5 years", "6 years", "7 years"]):
        experience_level = "Senior"
    elif any(x in lower for x in ["mid", "3 years", "4 years"]):
        experience_level = "Mid"
    elif any(x in lower for x in ["1 year", "2 years"]):
        experience_level = "Junior"

    strengths = []
    if any(word in lower for word in ["developed", "built", "implemented"]):
        strengths.append("Shows practical hands-on development experience.")
    if any(word in lower for word in ["collaborated", "team", "teamwork"]):
        strengths.append("Mentions collaboration and working well with teams.")
    if any(word in lower for word in ["test", "jest", "coverage"]):
        strengths.append("Includes attention to quality and testing.")

    improvements = []
    if "summary" not in lower and "profile" not in lower:
        improvements.append("Add a short professional summary at the top.")
    if not skills_found:
        improvements.append("Add a clear Skills section showing your technologies.")
    if all(x not in lower for x in ["%", "percent", "increased", "improved"]):
        improvements.append("Use metrics to quantify achievements.")
    if "education" not in lower and "bachelor" not in lower and "degree" not in lower:
        improvements.append("Include an Education section with degree and school.")

    suggested_roles = []
    if any(kw in lower for kw in ["react", "typescript", "javascript"]):
        suggested_roles.append("Frontend Developer")
    if any(kw in lower for kw in ["node", "express", "api"]):
        suggested_roles.append("Backend Developer")
    if any(kw in lower for kw in ["python", "sql", "postgresql"]):
        suggested_roles.append("Full Stack Developer")
    if not suggested_roles:
        suggested_roles.append("Software Engineer")

    result = [
        f"Key Skills found: {', '.join(skills_found) if skills_found else 'No clear technical skills detected.'}",
        f"Experience Level: {experience_level}",
        "Strengths:",
    ]
    if strengths:
        result.extend([f"- {s}" for s in strengths])
    else:
        result.append("- Clear technical experience is described.")

    if improvements:
        result.append("Areas to improve:")
        result.extend([f"- {item}" for item in improvements])

    result.append("Suggested roles:")
    result.extend([f"- {role}" for role in sorted(set(suggested_roles))])

    return "\n".join(result)


def analyse_resume(resume_text: str) -> str:
    try:
        chain = _build_chain()
        response = chain.invoke({"resume_text": resume_text})
        return response.content
    except Exception:
        return _heuristic_resume_analysis(resume_text)