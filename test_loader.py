from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("app/documents/company_policy.pdf")

documents = loader.load()

print(documents[0].page_content)
print(documents[0].metadata)