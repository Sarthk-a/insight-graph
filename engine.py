import os
from dotenv import load_dotenv
from utils import get_retriever
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

# Load API keys from .env
load_dotenv()

# Initialize AI and Tools
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
search = TavilySearch(max_results=2)
retriever = get_retriever("chart.pdf") 

def run_researcher(query):
    print(f"\n--- Analyzing Query: '{query}' ---")
    
    # Step 1: Look in the PDF
    docs = retriever.invoke(query)
    context = "\n".join([d.page_content for d in docs])
    
    # Step 2: The Agentic Decision
    check = llm.invoke(f"Is this text enough to answer '{query}'? Reply YES/NO: {context}")
    
    if "NO" in check.content.upper():
        print("--- Info missing from PDF. Transitioning to Web Search... ---")
        web = search.invoke(query)
        context += f"\nWeb Data: {web}"
    else:
        print("--- Answer found in PDF. Generating response... ---")
        
    # Step 3: Final Answer
    return llm.invoke(f"Context: {context}\nQuestion: {query}").content

if __name__ == "__main__":
    print("Agent Initialized. Ready for questions.")
    while True:
        user_query = input("\nAsk a question (or type 'exit'): ")
        if user_query.lower() == 'exit':
            break
        print("\nResponse:\n", run_researcher(user_query))