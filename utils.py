import os
import base64
from io import BytesIO
from dotenv import load_dotenv # <-- Add this
from pdf2image import convert_from_path
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load the keys BEFORE starting the AI!
load_dotenv() # <-- Add this

# We need the Brain to "see" during the database creation
vision_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
def analyze_image(image):
    """Takes a single page image, asks Gemini for chart data."""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Describe any charts, graphs, or visual data on this page in extreme detail. Include numbers and axes. If there are no charts, reply strictly with the word: NONE"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
        ]
    )
    
    response = vision_llm.invoke([message])
    return response.content

def get_retriever(pdf_path):
    print("\n--- 1. Reading PDF Text ---")
    loader = PyPDFLoader(pdf_path)
    pages = loader.load() # Load pages as LangChain Documents
    
    print("--- 2. Slicing PDF for Vision Analysis ---")
    # For this test, we will only process the first 3 pages to save time/API limits
    images = convert_from_path(pdf_path, first_page=1, last_page=3)
    
    print("--- 3. Merging Vision Data into Text Data ---")
    for i, image in enumerate(images):
        print(f"   Analyzing Page {i+1}...")
        vision_text = analyze_image(image)
        
        if "NONE" not in vision_text.upper():
            print(f"   -> Found visual data on Page {i+1}! Injecting into memory.")
            # Glue the vision description to the bottom of the page's text
            pages[i].page_content += f"\n\n[VISUAL DATA ON THIS PAGE]:\n{vision_text}"
            
    print("--- 4. Building Vector Database ---")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = Chroma.from_documents(pages, embeddings)
    
    return vectorstore.as_retriever(search_kwargs={"k": 2})