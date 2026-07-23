from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import GEMINI_API_KEY


embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
)

vector_store = FAISS.load_local(
    folder_path="faiss_index",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True,
)

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 2
    }
)