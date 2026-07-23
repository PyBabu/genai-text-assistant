from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

from app.database import SessionLocal
from app.rag.rag_service import ask_rag, stream_rag
from app.services.chat_history_service import (
    load_messages,
    save_message,
)


chat_history = {}


def get_history(session_id: str):

    if session_id not in chat_history:

        history = InMemoryChatMessageHistory()

        db = SessionLocal()

        try:

            messages = load_messages(
                db=db,
                session_id=session_id,
            )

            for message in messages:

                if message.role == "human":
                    history.add_message(
                        HumanMessage(content=message.message)
                    )

                else:
                    history.add_message(
                        AIMessage(content=message.message)
                    )

        finally:
            db.close()

        chat_history[session_id] = history

    return chat_history[session_id]


def ask_llm(
    question: str,
    session_id: str,
):

    history = get_history(session_id)

    history_text = "\n".join(
        f"{message.type}: {message.content}"
        for message in history.messages
    )

    answer = ask_rag(
        question=question,
        history=history_text,
    )

    history.add_message(
        HumanMessage(content=question)
    )

    history.add_message(
        AIMessage(content=answer)
    )

    db = SessionLocal()

    try:

        save_message(
            db=db,
            session_id=session_id,
            role="human",
            message=question,
        )

        save_message(
            db=db,
            session_id=session_id,
            role="ai",
            message=answer,
        )

    finally:
        db.close()

    return answer


def stream_llm(
    question: str,
    session_id: str,
):

    history = get_history(session_id)

    history_text = "\n".join(
        f"{message.type}: {message.content}"
        for message in history.messages
    )

    full_answer = ""

    for chunk in stream_rag(
        question=question,
        history=history_text,
    ):

        chunk = str(chunk)

        full_answer += chunk

        yield chunk

    history.add_message(
        HumanMessage(content=question)
    )

    history.add_message(
        AIMessage(content=full_answer)
    )

    db = SessionLocal()

    try:

        save_message(
            db=db,
            session_id=session_id,
            role="human",
            message=question,
        )

        save_message(
            db=db,
            session_id=session_id,
            role="ai",
            message=full_answer,
        )

    finally:
        db.close()