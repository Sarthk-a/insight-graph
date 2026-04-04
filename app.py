import streamlit as st
import os
from engine import run_researcher
from utils import get_retriever

# 1. Setup the Page
st.set_page_config(page_title="Insight Graph", page_icon="✺", layout="centered")

# --- CSS Injection (Keeping your sleek dark mode!) ---
custom_css = """
<style>
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
        max-width: 800px;
    }
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 400;
        color: #e4e4e7;
        margin-top: 10vh;
        margin-bottom: 2rem;
        font-family: 'Georgia', serif;
    }
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- THE SIDEBAR UPLOADER ---
with st.sidebar:
    st.markdown("### 📂 Data Source")
    uploaded_file = st.file_uploader("Upload a PDF to analyze", type="pdf")
    st.markdown("---")
    st.markdown("💡 *The AI will read text, extract chart data, and fall back to web search if needed.*")

# --- DYNAMIC MEMORY CACHE ---
# By passing the raw bytes into this function, Streamlit is smart enough to know
# that if you upload a NEW file, the bytes change, so it will rebuild the database!
@st.cache_resource(show_spinner="Extracting Vision Data and Building Memory...")
def boot_ai_memory(file_bytes):
    # Save the uploaded file to a temporary location so our backend tools can read it
    temp_path = "temp_uploaded.pdf"
    with open(temp_path, "wb") as f:
        f.write(file_bytes)
        
    return get_retriever(temp_path)

# --- MAIN APP LOGIC ---
if uploaded_file is None:
    # State 1: Waiting for user to upload a document
    st.markdown("<h1 class='main-title'>✺ Waiting for Document...</h1>", unsafe_allow_html=True)
    st.info("👈 Please upload a PDF in the sidebar to begin.")

else:
    # State 2: Document uploaded, ready to chat
    st.markdown("<h1 class='main-title'>✺ Hello, night owl</h1>", unsafe_allow_html=True)
    
    # Load the specific file into the AI's brain
    agent_memory = boot_ai_memory(uploaded_file.getvalue())

    # Initialize Chat Memory
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Draw Previous Messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # The Chat Input Box
    if user_query := st.chat_input("Ask about the document or the live web..."):
        
        st.markdown("""<style>.main-title {display: none;}</style>""", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = run_researcher(user_query, agent_memory)
                st.markdown(response)
                
        st.session_state.messages.append({"role": "assistant", "content": response})