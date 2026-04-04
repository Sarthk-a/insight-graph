import os
import base64
from io import BytesIO
from dotenv import load_dotenv
from pdf2image import convert_from_path
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# We use the same brain, but now we use its "Eyes"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def analyze_pdf_image(pdf_path):
    print("--- 1. Slicing PDF into images... ---")
    # Convert just the first page to an image
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    first_page_img = images[0]
    
    print("--- 2. Formatting image for AI... ---")
    # Convert the image to a Base64 string (how APIs read images)
    buffered = BytesIO()
    first_page_img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    print("--- 3. Pushing to Gemini Vision... ---")
    # This is the Multimodal LangChain syntax
    message = HumanMessage(
        content=[
            {"type": "text", "text": "You are a financial and data analyst. Look at this page. Describe every chart, graph, or diagram you see in extreme detail. Include the numbers, axis labels, and trends. If there are no charts, just say 'No visual data found'."},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
        ]
    )
    
    response = llm.invoke([message])
    return response.content

if __name__ == "__main__":
    if os.path.exists("chart.pdf"):
        print("\nAI Vision Analysis:\n")
        print(analyze_pdf_image("chart.pdf"))
    else:
        print("ERROR: Please upload a file named 'chart.pdf' first!")