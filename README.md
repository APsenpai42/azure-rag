# Project Title

A FastAPI-based Web Application for Retrieval-Augmented Generation (RAG) using Qdrant and Local LlamaFile

## Project Overview

This project updates an existing Azure-based Retrieval-Augmented Generation (RAG) web application by integrating the Qdrant vector database and a local LlamaFile model. The updates include:

- Replacing Azure services with a local LlamaFile for text generation.
- Generating and storing embeddings in Qdrant.
- Using FastAPI to verify the functionality of the RAG implementation via an interactive web interface.

## Key Features

- **Qdrant Integration**: Qdrant serves as the vector database for storing and querying text embeddings.
- **Local LlamaFile**: A lightweight, local alternative to Azure for generating responses.
- **FastAPI Interface**: An intuitive API for interacting with the RAG setup.
- **Easy Verification**: Access the `/docs` URL to test the `/ask` endpoint.

## Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Required Python dependencies (listed in `requirements.txt`)

## Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/APsenpai42/azure-rag
cd azure-rag
```

### Step 2: Set Up the Environment

1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate # On Windows, use .venv\Scripts\activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the local Llamafile.


4. Update the `.env` file to point to your local LlamaFile. Example:
   ```env
   LLAMAFILE_API_URL=http://127.0.0.1:8080  # Update with your Llamafile server URL
   LLAMAFILE_API_KEY="your-llamafile-api-key"  # Replace with your actual API key if required
   ```

### Step 3: Generate and Load Embeddings

For this project, we are using an in-memory Qdrant instance.
The embeddings will be automatically loaded when running the application.


### Step 4: Run the FastAPI Application

Start the application using Uvicorn:
```bash
uvicorn main:app --reload
```

### Step 5: Verify the RAG Functionality

1. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

2. Interact with the `/ask` endpoint by providing a query.

## Testing and Validation

- Use the `/ask` endpoint to send queries and verify responses.
- Confirm that embeddings are correctly stored and retrieved from Qdrant.

## Acknowledgments
- [Parent repository(Azure based)](https://github.com/alfredodeza/azure-rag)
- [LLaMA file repository](https://github.com/Mozilla-Ocho/llamafile?tab=readme-ov-file)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [LlamaFile Documentation](https://github.com/llamaindex/llamafiles)