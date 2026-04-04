# Insight Graph Analyst

This is a multimodal Retrieval-Augmented Generation (RAG) pipeline. It reads documents, extracts text descriptions from embedded charts and graphs using vision models, and autonomously searches the internet when its local knowledge falls short.

## Features

* **Multimodal RAG:** Uses vision models to parse PDFs and extract data from visual elements, rather than just reading plain text.
* **Agentic Routing:** The agent evaluates its own local vector memory. If it cannot answer a question based on the uploaded document, it automatically falls back to web search to find the answer.
* **Local Vector Storage:** Uses ChromaDB for fast, in-memory semantic search.
* **Cloud-Ready Setup:** Built to run in GitHub Codespaces to avoid local C++ dependency headaches (specifically with the Poppler engine).
* **Web UI:** Includes a Streamlit frontend for interacting with the agent outside the terminal.

## Tech Stack

* **LLM & Vision:** Google gemini-2.5-flash
* **Embeddings:** Google gemini-embedding-001
* **Web Search:** Tavily API (langchain-tavily)
* **Framework:** LangChain
* **Vector Database:** Chroma
* **Frontend:** Streamlit
* **PDF Parsing:** pdf2image & Poppler


License
MIT License
---



