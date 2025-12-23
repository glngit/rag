"""Rebuild FAISS index from the data/ folder.

Usage (PowerShell):
    python .\scripts\rebuild_index.py

This will print which files were found by the data loader and recreate the `faiss_store` with
`faiss.index` and `metadata.pkl` so newly added PDFs are included.
"""
from pathlib import Path
import sys

# Adjust path so project root modules import correctly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore

DATA_DIR = "data"
PERSIST_DIR = "faiss_store"

if __name__ == "__main__":
    print(f"[INFO] Rebuilding FAISS index from data folder: {Path(DATA_DIR).resolve()}")
    docs = load_all_documents(DATA_DIR)
    print(f"[INFO] Documents loaded: {len(docs)}")
    store = FaissVectorStore(persist_dir=PERSIST_DIR)
    store.build_from_documents(docs)
    print("[INFO] Rebuild complete.")
