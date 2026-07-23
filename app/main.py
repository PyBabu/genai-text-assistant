from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from app.database import Base
from app.database import engine
from app.schemas.chat import ChatRequest
from app.services.llm_service import ask_llm, stream_llm

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Welcome to GenAI Text Assistant"}


@app.post("/chat")
def chat(request: ChatRequest):

    answer = ask_llm(
        request.question,
        request.session_id
    )

    return {
        "answer": answer
    }


@app.post("/chat-stream")
def chat_stream(request: ChatRequest):

    return StreamingResponse(
        stream_llm(
            request.question,
            request.session_id
        ),
        media_type="text/plain"
    )




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Later change to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)