import streamlit as st
import random
import json
import os
from datetime import datetime

st.set_page_config(page_title="🤖 بوت دردشة ذكي يشبه ChatGPT", page_icon="🤖", layout="centered")

# ---------- CSS ----------
st.markdown("""
    <style>
        html, body {
            background-color: #0e1117;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        .chat-message {
            padding: 12px 18px;
            margin: 12px 0;
            border-radius: 20px;
            font-size: 16px;
            line-height: 1.6;
            max-width: 70%;
            word-wrap: break-word;
            box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        }
        .user-message {
            background-color: #3c3c3c;
            color: #f5f5f5;
            margin-left: auto;
            text-align: right;
        }
        .bot-message {
            background-color: #1a1a1a;
            color: #ffffff;
            margin-right: auto;
            text-align: left;
        }
        .timestamp {
            font-size: 11px;
            color: #888;
            text-align: center;
            margin-top: -10px;
            margin-bottom: 10px;
        }
        textarea {
            font-size: 16px !important;
            padding: 12px !important;
            height: 80px !important;
            border-radius: 12px !important;
            background-color: #1f1f1f !important;
            color: #ffffff !important;
            border: 1px solid #444 !important;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------- Session ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "personality" not in st.session_state:
    st.session_state.personality = "مزاحي 😄"

if "username" not in st.session_state:
    st.session_state.username = "أنت"
if "botname" not in st.session_state:
    st.session_state.botname = "المساعد 🤖"

# ---------- Title ----------
st.markdown("<h1 style='text-align: center;'>🤖 بوت دردشة ذكي يشبه ChatGPT</h1>", unsafe_allow_html=True)

# ---------- User Settings ----------
with st.sidebar:
    st.text_input("🧍 اسمك:", value=st.session_state.username, key="username")
    st.text_input("🤖 اسم البوت:", value=st.session_state.botname, key="botname")
    st.selectbox("🎭 اختر شخصية البوت:", ["مزاحي 😄", "مبرمج 👨‍💻", "شاعر 📝", "طبيب نفسي 💬", "عراقي ابن محلة 😂"], key="personality")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        if os.path.exists("chat_memory.json"):
            os.remove("chat_memory.json")

# ---------- Functions ----------
def save_history():
    with open("chat_memory.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)

def generate_reply(msg):
    p = st.session_state.personality
    if msg.startswith("/clear"):
        st.session_state.messages = []
        return "✅ تم مسح المحادثة."
    if msg.startswith("/save"):
        save_history()
        return "📁 تم حفظ المحادثة."
    if p == "مزاحي 😄":
        return random.choice(["هههه ضحكتني 😂", "إنت رهيب والله 🤣", "جبتها يا مبدع 😆"])
    elif p == "مبرمج 👨‍💻":
        return "جرب هذا الكود:\n```python\nprint('Hello, world!')\n```"
    elif p == "شاعر 📝":
        return "أهلاً بمن طرق القصيدة... كلامك ورد، وحرفك عبير 🌸"
    elif p == "طبيب نفسي 💬":
        return "أنا وياك، كلشي يتصلّح، إنت قوي ومهم ❤️"
    elif p == "عراقي ابن محلة 😂":
        return "هااااااااااااا شبيك حبيبي شنو السؤال الخرافي 😎"
    else:
        return "رد عام من البوت."

# ---------- Display Messages ----------
for msg in st.session_state.messages:
    role = msg["role"]
    name = st.session_state.username if role == "user" else st.session_state.botname
    css = "user-message" if role == "user" else "bot-message"
    timestamp = f"<div class='timestamp'>{msg['time']}</div>"
    st.markdown(f"<div class='chat-message {css}'><b>{name}:</b><br>{msg['content']}</div>{timestamp}", unsafe_allow_html=True)

# ---------- Input ----------
user_input = st.chat_input("💬 اكتب رسالتك هنا...")

if user_input:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state.messages.append({"role": "user", "content": user_input, "time": now})
    reply = generate_reply(user_input)
    st.session_state.messages.append({"role": "bot", "content": reply, "time": now})
    save_history()
    st.rerun()


# ---------- Download Button ----------
if st.session_state.messages:
    full_text = "\n".join([f"[{m['time']}] {m['role']} - {m['content']}" for m in st.session_state.messages])
    st.download_button("⬇️ تحميل المحادثة كـ .txt", full_text, file_name="chat_history.txt")
