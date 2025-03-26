import streamlit as st
import uuid
import requests

st.set_page_config(
    page_title="Elastic Search Chatbot",
    page_icon=":robot_face:",
    layout="centered",
    initial_sidebar_state="auto"
)

session_id = str(uuid.uuid4())

url = "http://localhost:5678/webhook-test/c9baa6dc-ac80-487f-ae55-718b06264cf8"
if "history" not in st.session_state:
    st.session_state.history = []

st.title("Elastic Search ChatBot")

def send_message():
    user_input = st.session_state.user_input
    if user_input.strip():
        body = {
            "sessionId": session_id,
            "chatInput": user_input,
            "action": "sendMessage"
        }
        res = requests.post(url, json=body)

        if res.content:
            try:
                resp = res.json()
                st.session_state.history.append({
                    "question": user_input,
                    "answer": resp.get("output", "No response received")
                })
            except ValueError:
                st.session_state.history.append({
                    "question": user_input,
                    "answer": f"Error decoding JSON response: {res.text}"
                })
        else:
            st.session_state.history.append({
                "question": user_input,
                "answer": "Empty response from server"
            })

        st.session_state.user_input = ""

# Display chat history
st.write("### Chat History")
for chat in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(f"*You:* {chat['question']}")
    with st.chat_message("assistant"):
        st.markdown(chat["answer"])
st.sidebar.title("Chat History")
for i, chat in enumerate(st.session_state.history):
    with st.sidebar.expander(f"Chat {i+1}"):
        st.markdown(f"**You:** {chat['question']}")
        st.markdown(f"**Assistant:** {chat['answer']}")

user_input = st.text_input(
    "Type your question here...",
    key="user_input",
    placeholder="Ask me anything...",
    on_change=send_message
)
