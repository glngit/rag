import os
from src.search import RAGSearch

def main():
    # Initialize RAG search
    rag_search = RAGSearch(persist_dir="faiss_store")
    
    # Example queries
    queries = [
        "What is attention mechanism?",
        "Explain Material Science concepts",
        "Define composite materials"
    ]

    for q in queries:
        print(f"\n[INFO] Querying: '{q}'")
        summary = rag_search.search_and_summarize(q, top_k=3)
        print("Summary:", summary)

if __name__ == "__main__":
    main()
