from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

from app.core.config import GEMINI_API_KEY

loader = PyPDFLoader(
    "app/documents/company_policy.pdf"
)

documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY,
)

vector_db = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)

vector_db.save_local("faiss_index")

print("FAISS database created successfully!")