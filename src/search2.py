import os
from dotenv import load_dotenv
from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
import google.generativeai as genai
from typing import Optional

load_dotenv()

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_API_KEY_ENV = "GEN_API_KEY"


class RAGSearch:
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2"):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        faiss_index_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")

        if not (os.path.exists(faiss_index_path) and os.path.exists(meta_path)):
            print("[INFO] FAISS index not found, building vector store...")
            docs = load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            print(f"[INFO] FAISS index found at {faiss_index_path}, loading...")
            self.vectorstore.load()

        api_key = os.getenv(GEMINI_API_KEY_ENV)
        if not api_key:
            raise ValueError(f"Gemini API key not found in environment variable '{GEMINI_API_KEY_ENV}'")

        genai.configure(api_key=api_key)
        self.model_name = GEMINI_MODEL
        self.model = genai.GenerativeModel(self.model_name)
        print(f"[INFO] Gemini LLM initialized: {GEMINI_MODEL}")

    # --------------------------------------------------------------------------
    def _extract_response_text(self, response) -> Optional[str]:
        """Robust extraction of text from Gemini response."""
        try:
            # Normal case
            if hasattr(response, "text") and response.text:
                return response.text
        except Exception as e:
            print(f"[DEBUG] .text accessor failed: {e}")

        # Fallback: extract manually from candidates
        try:
            if hasattr(response, "candidates") and response.candidates:
                for cand in response.candidates:
                    # Skip incomplete or filtered outputs
                    if getattr(cand, "finish_reason", None) in [None, "STOP"]:
                        content = getattr(cand, "content", None)
                        if not content:
                            continue

                        # Handle if content is a list (modern SDK)
                        if isinstance(content, list):
                            texts = [p.text for p in content if hasattr(p, "text") and p.text]
                            if texts:
                                return "\n".join(texts)

                        # Handle if content has .parts (older SDKs)
                        if hasattr(content, "parts"):
                            texts = [p.text for p in content.parts if hasattr(p, "text") and p.text]
                            if texts:
                                return "\n".join(texts)
        except Exception as e:
            print(f"[DEBUG] Candidate parse failed: {e}")

        # Optional: inspect prompt feedback
        if hasattr(response, "prompt_feedback"):
            print(f"[DEBUG] prompt_feedback: {response.prompt_feedback}")

        return None

    # --------------------------------------------------------------------------
    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r.get("metadata", {}).get("text", "") for r in results if r.get("metadata")]
        if not texts:
            return "No relevant documents found."

        attempts = [(4000, 600), (2000, 400), (1000, 250)]

        for attempt_idx, (char_limit, max_tokens) in enumerate(attempts, start=1):
            # Build truncated context
            context = []
            total = 0
            for t in texts:
                if not t:
                    continue
                remain = char_limit - total
                if remain <= 0:
                    break
                snippet = t[:remain]
                context.append(snippet)
                total += len(snippet)
            context_text = "\n\n".join(context)

            prompt = (
                "You are a knowledgeable assistant that gives concise, factual answers based only on the reference text.\n"
                f"Question: {query}\n\n"
                f"Reference Text:\n{context_text}\n\n"
                "Answer clearly and directly, summarizing key information from the reference text."
            )

            print(f"[DEBUG] Attempt {attempt_idx}: char_limit={char_limit}, max_tokens={max_tokens}")

            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.1,
                        "top_p": 0.9,
                        "max_output_tokens": max_tokens,
                    },
                )

                text = self._extract_response_text(response)
                if text:
                    return text.strip()

                # Log diagnostic info
                if hasattr(response, "candidates") and response.candidates:
                    for i, c in enumerate(response.candidates):
                        print(f"[DEBUG] Candidate {i} finish_reason={getattr(c, 'finish_reason', None)}, "
                            f"safety_ratings={getattr(c, 'safety_ratings', None)}")

            except Exception as e:
                print(f"[ERROR] Gemini API error on attempt {attempt_idx}: {e}")
                continue

        return "Sorry — the model couldn't produce an answer. Try rephrasing your question."


# --------------------------------------------------------------------------
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
