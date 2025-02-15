import streamlit as st
from chatbot_service import Chatbot

# Page Config MUST be the first Streamlit command
st.set_page_config(page_title=" Wattmonk AI Assistant", layout="wide")

st.title(" Wattmonk AI Assistant")
st.write("Ask any question about Wattmonk's services or the solar industry.")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Dropdown for common questions
faq_questions = [
    "What services does Wattmonk offer?",
    "How does Wattmonk handle interconnection?",
    "What is the cost of solar installation?",
    "How does Wattmonk compare to Tesla Solar?",
    "How long does it take to get a solar permit?"
]

selected_question = st.selectbox("📌 Frequently Asked Questions:", ["Select a question"] + faq_questions)

# User input text box
user_input = st.text_input(" Your Question:", value=selected_question if selected_question != "Select a question" else "")

# Button layout: "Ask" and "Clear Chat"
col1, col2 = st.columns([0.7, 0.3])

with col1:
    ask_button = st.button("Ask")

with col2:
    clear_button = st.button("🗑 Clear Chat")

# Handle "Ask" button
if ask_button:
    if user_input.strip():  # Ensure input is not empty
        response = Chatbot(user_input)

        # Save chat history (latest message at the TOP)
        st.session_state.chat_history.insert(0, (" You:", user_input))
        st.session_state.chat_history.insert(0, (" AI:", response))

# Handle "Clear Chat" button
if clear_button:
    st.session_state.chat_history = []

# Display chat history with latest messages at the TOP
st.write("## Chat History")
for role, text in st.session_state.chat_history:
    st.markdown(f"**{role}** {text}")
