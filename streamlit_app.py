import streamlit as st
from dotenv import load_dotenv
from typing import List

load_dotenv()

from src.search import RAGSearch


@st.cache_resource
def get_rag():
    try:
        return RAGSearch(persist_dir="faiss_store")
    except Exception as e:
        # Re-raise so the UI can handle it
        raise


def main():
    st.set_page_config(
        page_title="RAG Research Assistant",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📚 Document Research Assistant")
    st.markdown("""
    Ask questions about your documents and get comprehensive answers.
    """)

    with st.sidebar:
        st.header("⚙️ Settings")
        # Using a fixed value for top_k since we're not showing sources
        top_k = 5
        clear = st.button("🗑️ Clear Chat History")

    if "history" not in st.session_state:
        st.session_state.history = []

    try:
        rag = get_rag()
    except Exception as e:
        st.error(f"⚠️ Failed initializing the research assistant: {e}")
        return

    with st.form(key="query_form"):
        query = st.text_area(
            "What would you like to know about?",
            height=100,
            placeholder="Enter your question here..."
        )

        submitted = st.form_submit_button("🔍 Search and Analyze", use_container_width=True)
        if submitted and query.strip():
            with st.spinner("🤔 Generating answer..."):
                summary = rag.search_and_summarize(query, top_k=top_k)
                st.session_state.history.append({"query": query, "summary": summary}) 

    # Show chat history (most recent first)
    for entry in reversed(st.session_state.history):
        st.markdown("---")
        with st.container():
            st.markdown(f"### ❓ {entry['query']}")
            st.markdown("### 📝 Answer:")
            # Display the answer in a cleaner way
            answer_container = st.container()
            with answer_container:
                st.markdown(entry['summary'])
                st.markdown("---")

    if clear:
        st.session_state.history = []
        st.experimental_rerun()


if __name__ == "__main__":
    main()
