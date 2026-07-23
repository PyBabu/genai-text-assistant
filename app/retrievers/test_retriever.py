from app.retrievers.retriever import retriever

query = "What are the office timings?"

documents = retriever.invoke(query)

for index, document in enumerate(documents, start=1):
    print(f"Document {index}")
    print(document.page_content)
    print("-" * 50)