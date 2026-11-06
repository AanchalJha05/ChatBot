
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Personality Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Load Gemini model
@st.cache_resource
def load_model():
    return init_chat_model(
        "google_genai:gemini-3.6-flash",
        thinking_level="low",
        max_tokens=512
    )

model = load_model()

# AI personalities
modes = {
    "Angry 😡": "You are an angry AI agent. You respond aggressively and impatiently.",
    "Funny 😂": "You are a very funny AI agent. You respond with humor and jokes.",
    "Sad 😢": "You are a very sad AI agent. You respond in a sad and emotional tone."
}

# Heading
st.title("🤖 AI Personality Chatbot")
st.write("Choose your AI personality and start chatting!")

st.divider()

# Select personality
st.subheader("Choose your AI mode")

choice = st.radio(
    "Select personality:",
    list(modes.keys()),
    horizontal=True
)

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=modes[choice])
    ]
    st.session_state.selected_mode = choice

# Reset history when personality changes
if st.session_state.selected_mode != choice:
    st.session_state.selected_mode = choice
    st.session_state.messages = [
        SystemMessage(content=modes[choice])
    ]

st.divider()

# Display conversation history
for message in st.session_state.messages:

    if isinstance(message, SystemMessage):
        continue

    role = "user" if isinstance(message, HumanMessage) else "assistant"

    content = message.content

    if isinstance(content, list):
        content = "".join(
            block["text"]
            for block in content
            if block.get("type") == "text"
        )

    with st.chat_message(role):
        st.markdown(content)

# Chat input
prompt = st.chat_input("Type your message here...")

if prompt:

    # Display user message
    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):

            with st.spinner("AI is thinking..."):

                response = model.invoke(
                    st.session_state.messages
                )

                st.session_state.messages.append(
                    AIMessage(content=response.content)
                )

                # Extract response text
                if isinstance(response.content, list):
                    answer = "".join(
                        block["text"]
                        for block in response.content
                        if block.get("type") == "text"
                    )
                else:
                    answer = response.content

                st.markdown(answer)

    except Exception as e:
        st.session_state.messages.pop()
        st.error(f"Error: {e}")
