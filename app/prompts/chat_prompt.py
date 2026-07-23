from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI Assistant.

Answer ONLY from the given context.

Context:
{context}

If the answer is not available in the context,
reply with:

"I don't know based on the provided document."
"""
        ),
        (
            "human",
            "{input}"
        )
    ]
)