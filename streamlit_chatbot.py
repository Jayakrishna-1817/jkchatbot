import streamlit as st
import google.generativeai as genai

# 🔹 Configure Gemini API Key (Replace with your actual key)
GENAI_API_KEY = "AIzaSyCuQlmk4Rvq-qR6dpP8JLRqNdl8BKlSGsw"  # Replace with your actual key
genai.configure(api_key=GENAI_API_KEY)

# 🔹 Load a valid Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")  # Updated model name

# 🔹 Streamlit UI with Custom CSS Fixes
st.markdown("""
    <style>
        /* 🔹 Page Background */
        body {
            background-color: #141e30;
            color: white;
        }

        /* 🔹 Custom chat bubble styling */
        .chat-bubble {
            padding: 12px;
            border-radius: 12px;
            margin: 10px 0;
            width: fit-content;
            max-width: 80%;
        }

        .user-message {
            background-color: rgba(0, 150, 255, 0.3);
            text-align: right;
            float: right;
        }

        .assistant-message {
            background-color: rgba(0, 255, 150, 0.3);
            text-align: left;
            float: left;
        }

        /* 🔹 Typing animation */
        @keyframes typing {
            0% { opacity: 0.3; }
            50% { opacity: 1; }
            100% { opacity: 0.3; }
        }

        .assistant-message.typing {
            animation: typing 1.2s steps(30, end) infinite;
        }

        /* 🔹 Glowing input field */
        input {
            border-radius: 8px;
            border: 2px solid #00bcd4;
            transition: 0.3s;
        }

        input:hover, input:focus {
            border-color: #ff4081;
            box-shadow: 0 0 10px #ff4081;
        }

        /* 🔹 Title bounce effect */
        h1 {
            animation: bounceIn 1s ease-in-out;
            text-align: center;
            font-size: 2.5em;
            color: #00e5ff;
        }

        @keyframes bounceIn {
            0% { transform: scale(0.9); opacity: 0; }
            60% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 Chat with JK's Bot</h1>", unsafe_allow_html=True)

# 🔹 Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Display previous messages
for msg in st.session_state.messages:
    role_class = "user-message" if msg["role"] == "user" else "assistant-message"
    st.markdown(f'<div class="chat-bubble {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# 🔹 Accept user input
if user_input := st.chat_input("Ask me anything..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    st.markdown(f'<div class="chat-bubble user-message">{user_input}</div>', unsafe_allow_html=True)

    # 🔹 Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = model.generate_content(user_input)
            bot_reply = response.text
        except Exception as e:
            bot_reply = f"⚠️ Error: {e}"

        # Display response with custom styling
        message_placeholder.markdown(f'<div class="chat-bubble assistant-message">{bot_reply}</div>', unsafe_allow_html=True)

    # Save AI response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
