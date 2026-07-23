from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

from langchain_community.vectorstores import FAISS

from app.core.config import GEMINI_API_KEY
from app.prompts.chat_prompt import chat_prompt


# Create LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GEMINI_API_KEY,
)

# Create Embedding Model
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GEMINI_API_KEY,
)

# Load FAISS Database
vector_db = FAISS.load_local(
    "faiss_index",
    embedding_model,
    allow_dangerous_deserialization=True,
)

# Create Retriever
retriever = vector_db.as_retriever(
    search_kwargs={"k": 2}
)

# Create Document Chain
document_chain = create_stuff_documents_chain(
    llm,
    chat_prompt,
)

# Create Retrieval Chain
rag_chain = create_retrieval_chain(
    retriever,
    document_chain,
)


def ask_pdf(question: str):
    response = rag_chain.invoke(
        {
            "input": question
        }
    )

    return response["answer"]