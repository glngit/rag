# Quick Start Guide - Setting Up RAG App on a New VM

This guide walks you through setting up and running the RAG (Retrieval-Augmented Generation) application from scratch on a new virtual machine.

## Prerequisites

- Python 3.10 or higher
- pip package manager
- ~5GB disk space (for dependencies and models)
- API keys (optional, depending on which LLM you want to use):
  - Google Generative AI API key
  - OpenAI API key
  - Groq API key

## Step 1: Clone/Download the Project

```bash
cd ~/Documents
# Clone or navigate to the project directory
cd rag
```

## Step 2: Create a Python Virtual Environment

```bash
# Create virtual environment named 'venv'
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

**On Windows, use:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt when activated.

## Step 3: Install Project Dependencies

```bash
# Make sure you're in the project root directory
# and the venv is activated

pip install -r requirements.txt
```

This will install all required packages including:
- LangChain & LangGraph
- Sentence Transformers
- FAISS (vector database)
- Streamlit (web framework)
- PyPDF & PyMuPDF (document processing)
- ChromaDB, Groq, OpenAI, Google Generative AI

The installation may take 5-15 minutes depending on your internet speed.

## Step 4: Set Up Environment Variables

```bash
# Copy the template .env file if it exists, or create your own
cp .env.example .env  # if template exists

# OR create a new .env file
nano .env
```

Add your API keys:
```
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

Save and exit (Ctrl+X, then Y in nano).

## Step 5: Build the Vector Store

The first time you run the app, you need to build the vector store from your documents:

```bash
# Make sure venv is activated
python scripts/rebuild_index.py
```

This will:
1. Load documents from the `data/` directory
2. Split them into chunks
3. Generate embeddings using `all-MiniLM-L6-v2`
4. Create a FAISS index
5. Save everything to `faiss_store/`

**Expected output:**
```
[INFO] Loaded embedding model: all-MiniLM-L6-v2
[INFO] Building vector store from X raw documents...
[INFO] Split X documents into Y chunks.
[INFO] Generating embeddings for Y chunks...
[INFO] Added Y vectors to Faiss index.
[INFO] Saved Faiss index and metadata to faiss_store
[INFO] Vector store built and saved to faiss_store
```

## Step 6: Run the Streamlit App

```bash
# Make sure venv is activated
streamlit run streamlit_app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://your.ip.address:8501
```

Open your browser and go to `http://localhost:8501`

## Step 7: Interact with the App

In the Streamlit interface:
1. **Enter a query** in the text input (e.g., "What is attention mechanism?")
2. **Adjust settings** like:
   - Number of documents to retrieve (top_k)
   - LLM selection (OpenAI, Groq, Google, etc.)
3. **View results**:
   - Retrieved documents
   - Generated summary
   - Citation sources

## Troubleshooting

### Virtual Environment Not Activating
```bash
# Try the full path
source ./venv/bin/activate

# Or reinstall venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

### Missing Dependencies
```bash
# Reinstall all requirements
pip install --upgrade -r requirements.txt
```

### FAISS Index Not Found
```bash
# Rebuild the vector store
python scripts/rebuild_index.py
```

### Port 8501 Already in Use
```bash
# Run on a different port
streamlit run streamlit_app.py --server.port 8502
```

### Out of Memory
The embedding model loads ~350MB into memory. If you have <2GB RAM available:
- Close other applications
- Or reduce the number of documents in `data/pdf/`

## Alternative: Run Command-Line App

Instead of Streamlit, you can run the CLI version:

```bash
python app.py
```

This will execute example queries and print results to the terminal.

## Deactivating Virtual Environment

When you're done:
```bash
deactivate
```

## Next Time You Use This VM

```bash
cd ~/Documents/rag
source venv/bin/activate
streamlit run streamlit_app.py
```

That's it! You're ready to go.

## Project Structure

```
rag/
├── streamlit_app.py      # Main web app
├── app.py                # CLI version
├── main.py               # Simple test script
├── requirements.txt      # Python dependencies
├── .env                  # API keys (create this)
├── data/pdf/             # Your documents (PDFs)
├── faiss_store/          # Vector database (created by rebuild_index.py)
├── src/
│   ├── search.py         # RAG search logic
│   ├── embedding.py      # Embedding functions
│   ├── data_loader.py    # Document loading
│   └── vectorstore.py    # Vector store management
├── scripts/
│   └── rebuild_index.py  # Build vector store script
└── notebook/             # Jupyter notebooks for exploration
```

## Support

For detailed information, check the main [README.md](README.md)
