from sqlalchemy.orm import Session

from app.models.chat_history import ChatHistory


def save_message(
    db: Session,
    session_id: str,
    role: str,
    message: str,
):

    chat = ChatHistory(
        session_id=session_id,
        role=role,
        message=message,
    )

    db.add(chat)
    db.commit()


def load_messages(
    db: Session,
    session_id: str,
):

    return (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.id.asc())
        .all()
    )