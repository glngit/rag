import os
from dotenv import load_dotenv
from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
import google.generativeai as genai  # Updated import

load_dotenv()

# Gemini model and API key environment variable
GEMINI_MODEL = "gemini-2.5-flash"  # Replace with your Gemini model
GEMINI_API_KEY_ENV = "GEN_API_KEY"  # Env var storing your Gemini key


class RAGSearch:
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", use_dockling: bool = True):
        """
        Initialize RAG Search with optional Dockling support.
        
        Args:
            persist_dir: Directory for storing FAISS index
            embedding_model: Embedding model to use
            use_dockling: If True, use Dockling for enhanced document understanding
        """
        # Load or build vector store
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        faiss_index_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")

        if not (os.path.exists(faiss_index_path) and os.path.exists(meta_path)):
            print("[INFO] FAISS index not found, building vector store...")
            # Load documents with optional Dockling enhancement
            docs = load_all_documents("data", use_dockling=use_dockling)
            self.vectorstore.build_from_documents(docs)
        else:
            print(f"[INFO] FAISS index found at {faiss_index_path}, loading...")
            self.vectorstore.load()

        # Configure Gemini API
        api_key = os.getenv(GEMINI_API_KEY_ENV)
        if not api_key:
            raise ValueError(f"Gemini API key not found in environment variable '{GEMINI_API_KEY_ENV}'")

        genai.configure(api_key=api_key)
        self.model_name = GEMINI_MODEL
        self.model = genai.GenerativeModel(self.model_name)

        print(f"[INFO] Gemini LLM initialized: {GEMINI_MODEL}")
        print(f"[INFO] Document understanding: {'Dockling' if use_dockling else 'Standard loaders'}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        # Step 1: Retrieve top documents from FAISS
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)

        if not context:
            return "No relevant documents found."

        # Step 2: Prepare prompt for Gemini
        prompt = f"""
        You are a helpful assistant. Summarize the following context and answer the query below.

        Query: {query}

        Context:
        {context}

        Summary:
        """

        # ✅ Step 3: Correct Gemini API call
        response = self.model.generate_content(
            prompt,
            generation_config={"temperature": 0.2}
        )

        return response.text


# Optional: interactive mode
if __name__ == "__main__":
    rag_search = RAGSearch()
    print("\n[INFO] Interactive RAG search ready. Type your query (or 'exit' to quit):\n")
    while True:
        query = input("Enter your query: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("[INFO] Exiting interactive search.")
            break
        summary = rag_search.search_and_summarize(query, top_k=3)
        print(f"\n[SUMMARY] {summary}\n{'-'*80}\n")
