import streamlit as st
from engine import run_researcher

# 1. Setup the Page
st.set_page_config(page_title="Insight Graph Analyst", page_icon="📊", layout="centered")
st.title("📊 Insight Graph Analyst")
st.markdown("An Agentic AI that reads your Multimodal PDFs and searches the web.")

# 2. Initialize Chat Memory
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! Ask me about your PDF or the live web."}]

# 3. Draw Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. The Chat Input Box
if user_query := st.chat_input("Ask a question (e.g., What was the exchange rate in 2016?)"):
    
    # Draw user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Draw assistant response
    with st.chat_message("assistant"):
        # Show a loading spinner while your engine runs
        with st.spinner("Analyzing document and searching the web..."):
            # This calls the engine you built!
            response = run_researcher(user_query)
            st.markdown(response)
            
    # Save the assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})