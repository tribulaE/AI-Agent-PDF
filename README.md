## RAG AI AGENT

Streamlit app that lets you upload a PDF, indexes it into a Qdrant vector database using OpenAI, then answers questions RAG

## Live Demo
https://tribulae-ai-agent-pdf-streamlit-app-s6hqro.streamlit.app/


## How it works
- Upload a pdf
- Splits text into chunks
- Creates embeddings from OpenAI
- Stores vectors + metadata in Qdrant
- Retrieves top-k relevant chunks for a user question
- Generates an answer and shows sources

## Stack
- Streamlit
- Inngest
- Docker
- Qdrant




