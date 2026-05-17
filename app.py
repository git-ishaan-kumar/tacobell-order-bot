import streamlit as st
import bot

# Page Setup
st.set_page_config(page_title="🌮 Taco Bell Order Bot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = bot.reset_chat_context()
    st.session_state.ui_messages = []
    st.session_state.cart = None

# Greeting
if not st.session_state.ui_messages:
    greeting = bot.get_greeting(st.session_state.chat_history)
    st.session_state.ui_messages.append({"role": "assistant", "content": greeting})

# Sidebar Info
st.sidebar.markdown("# 🌮 Taco Bell Order Bot")
st.sidebar.write(
    "A simulation of a chat bot that takes Taco Bell orders. Users can add, remove, and edit items on their order using a mock Taco Bell menu."
)

# Chat Bot Limits
order_started = len(st.session_state.ui_messages) > 1
limit_exceeded = len(st.session_state.ui_messages) >= 20

# Sidebar Restart
if order_started and st.session_state.cart is None and not limit_exceeded:
    if st.sidebar.button("🔄 Restart Order"):
        st.session_state.chat_history = bot.reset_chat_context()
        st.session_state.ui_messages = []
        st.session_state.cart = None
        st.rerun()

# Sidebar Buttons

# st.sidebar.markdown('<a href="https://youtube.com" target="_blank" style="text-decoration: none; display: block;"><div style="background-color: #21262d; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; display: flex; align-items: center; border: 1px solid #30363d; font-family: sans-serif; font-size: 14px; font-weight: 500;"><img src="https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg" style="width: 24px; height: 17px; margin-right: 10px;">Watch Video Demo</div></a>', unsafe_allow_html=True)
st.sidebar.markdown('<a href="https://github.com/git-ishaan-kumar/tacobell-order-bot/tree/main" target="_blank" style="text-decoration: none;"><div style="background-color: #21262d; color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; display: flex; align-items: center; border: 1px solid #30363d; font-family: sans-serif; font-size: 14px; font-weight: 500;"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" style="width: 20px; height: 20px; margin-right: 10px; filter: invert(1);">Open in GitHub</div></a>', unsafe_allow_html=True)

# Header
st.header("💬 Order Bot")

# Chat
for msg in st.session_state.ui_messages:
    avatar = "🌮" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Bot Response
if st.session_state.ui_messages[-1]["role"] == "user" and st.session_state.cart is None and not limit_exceeded:
    with st.chat_message("assistant", avatar="🌮"):
        with st.spinner("Thinking..."):
            response, cart = bot.bot_response(st.session_state.chat_history, st.session_state.ui_messages[-1]["content"])
            st.write(response)
    st.session_state.ui_messages.append({"role": "assistant", "content": response})
    if cart:
        st.session_state.cart = cart
    st.rerun()

# Order Summary
if st.session_state.cart is not None:
    st.subheader("🛍️ Final Receipt")
    st.json(st.session_state.cart)
    if st.button("🛒 Order Again"):
        st.session_state.chat_history = bot.reset_chat_context()
        st.session_state.ui_messages = []
        st.session_state.cart = None
        st.rerun()
    st.chat_input("Order Complete", disabled=True)

# Limit Hit
elif limit_exceeded:
    st.warning("⚠️ Maximum order length reached to prevent token abuse.")
    if st.button("🔄 Start New Order"):
        st.session_state.chat_history = bot.reset_chat_context()
        st.session_state.ui_messages = []
        st.session_state.cart = None
        st.rerun()
    st.chat_input("Order Limit Reached", disabled=True)

# User Input
else:
    user_input = st.chat_input("Ask Order Bot")
    if user_input:
        st.session_state.ui_messages.append({"role": "user", "content": user_input})
        st.rerun()