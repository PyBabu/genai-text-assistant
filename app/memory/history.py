from langchain_core.chat_history import InMemoryChatMessageHistory

# Dictionary to store all chat sessions
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]