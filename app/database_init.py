from app.database import Base
from app.database import engine

from app.models.chat_history import ChatHistory


Base.metadata.create_all(bind=engine)

print("Database Created Successfully")