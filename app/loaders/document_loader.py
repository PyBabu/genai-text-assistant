from langchain_community.document_loaders import PyPDFLoader


loader = PyPDFLoader(
    "app/documents/company_policy.pdf"
)

documents = loader.load()

print(documents)