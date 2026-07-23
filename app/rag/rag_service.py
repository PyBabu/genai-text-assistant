from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import GEMINI_API_KEY
from app.retrievers.retriever import retriever

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.3,
)


def build_context(question: str):
    documents = retriever.invoke(question)
    return "\n\n".join(doc.page_content for doc in documents)


def _extract_text(content):
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text = ""
        for item in content:
            if isinstance(item, dict):
                text += item.get("text", "")
            elif hasattr(item, "text"):
                text += item.text
            else:
                text += str(item)
        return text
    if hasattr(content, "text"):
        return content.text
    return str(content)


def ask_rag(question: str, history: str = ""):
    context = build_context(question)

    if context.strip():
        prompt = ChatPromptTemplate.from_template(
"""
You are a helpful AI Assistant.

Use the conversation history and context to answer the user's question.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer naturally and clearly.
"""
        )

        response = (prompt | llm).invoke(
            {
                "history": history,
                "context": context,
                "question": question,
            }
        )
    else:
        prompt = ChatPromptTemplate.from_template(
"""
You are a helpful AI Assistant.

Conversation History:
{history}

Question:
{question}

Answer using your general knowledge.
"""
        )

        response = (prompt | llm).invoke(
            {
                "history": history,
                "question": question,
            }
        )

    return _extract_text(response.content).strip()


def stream_rag(question: str, history: str = ""):
    context = build_context(question)

    if context.strip():
        prompt = ChatPromptTemplate.from_template(
"""
You are a helpful AI Assistant.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer naturally and clearly.
"""
        )

        stream = (prompt | llm).stream(
            {
                "history": history,
                "context": context,
                "question": question,
            }
        )
    else:
        prompt = ChatPromptTemplate.from_template(
"""
You are a helpful AI Assistant.

Conversation History:
{history}

Question:
{question}

Answer using your general knowledge.
"""
        )

        stream = (prompt | llm).stream(
            {
                "history": history,
                "question": question,
            }
        )

    for chunk in stream:
        text = _extract_text(chunk.content)
        if text:
            yield text
