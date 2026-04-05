Insight Graph
Multimodal RAG Agent with Vision-Enhanced Document Intelligence

Insight Graph is a research tool designed to solve a specific problem in document analysis: standard text parsers are blind to visual data. By combining LangChain with Google’s Gemini 2.5 Flash Lite, this application treats PDFs as images to extract data from charts, tables, and diagrams that traditional RAG pipelines usually ignore.

The Engineering Workflow
The application follows a multi-stage pipeline to build its "memory":

Visual Processing: Instead of just reading text, the app uses pdf2image to slice the document into high-resolution frames.

Vision Extraction: Gemini 2.5 Flash Lite analyzes these frames, generating detailed text descriptions of any axes, trendlines, or numerical data found in charts.

Hybrid Indexing: These visual descriptions are merged with the raw extracted text and embedded into a ChromaDB vector store.

Agentic Logic: A researcher agent handles the queries. It first attempts to answer using the document's vector memory but is programmed to trigger a live web search if the document context is insufficient.

Technical Architecture
Frontend: Streamlit (Customized with CSS for a minimal dark interface)

Logic: LangChain (Used for document loading, splitting, and agent orchestration)

Model: Google Gemini 2.5 Flash Lite (Chosen specifically to provide a high 1,000 requests/day quota on the free tier)

Vector Store: ChromaDB

Vision: pdf2image + poppler-utils

Critical Design Choices
Quota Management: During development, we pivoted from Gemini 2.5 Flash to the Lite version. This was a strategic decision to bypass the 20-request daily limit of the standard model, allowing for continuous testing and multiple document uploads.

Context Splicing: By injecting visual descriptions directly into the text chunks before embedding, we ensure the retriever can find "images" based on natural language questions.

Statelessness: The app uses Streamlit’s cache_resource to manage the vector database in memory, ensuring fast response times without the overhead of a permanent external database.
