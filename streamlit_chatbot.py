import streamlit as st
import requests

# 🔹 Configure Voiceflow API Key (Replace with your actual key)
VOICEFLOW_API_KEY = "VF.DM.67cb43277d87a3d423e8c128.iikFz5hVETfN02R7"  # Replace with your actual Voiceflow API Key
USER_ID = "test_user"  # Unique user ID to track conversations

# 🔹 Function to get a response from Voiceflow

def chat_with_voiceflow(prompt):
    url = f"https://general-runtime.voiceflow.com/state/user/{USER_ID}/interact"
    headers = {
        "Authorization": VOICEFLOW_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"action": {"type": "text", "payload": prompt}}
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()[0]["payload"]["message"]
    else:
        return f"⚠️ Error: {response.status_code} - {response.text}"

# 🔹 Streamlit UI
st.markdown("""
    <style>
        h1 { text-align: center; color: #00e5ff; }
        .chat-bubble { padding: 12px; border-radius: 12px; margin: 10px 0; max-width: 80%; }
        .user-message { background-color: rgba(0, 150, 255, 0.3); text-align: right; float: right; }
        .assistant-message { background-color: rgba(0, 255, 150, 0.3); text-align: left; float: left; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 Chat with Phani's Bot</h1>", unsafe_allow_html=True)

# 🔹 Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔹 Display previous messages
for msg in st.session_state.messages:
    role_class = "user-message" if msg["role"] == "user" else "assistant-message"
    st.markdown(f'<div class="chat-bubble {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# 🔹 Accept user input
if user_input := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble user-message">{user_input}</div>', unsafe_allow_html=True)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            bot_reply = chat_with_voiceflow(user_input)
        except Exception as e:
            bot_reply = f"⚠️ Error: {e}"
        
        message_placeholder.markdown(f'<div class="chat-bubble assistant-message">{bot_reply}</div>', unsafe_allow_html=True)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

