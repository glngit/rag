# Dockling Integration Guide

This project now includes **Dockling** for superior document understanding and content extraction.

## What is Dockling?

Dockling is a state-of-the-art document understanding library that uses advanced machine learning to extract and structure content from PDFs and images with better accuracy than traditional methods.

### Key Features:
- **Advanced Layout Understanding**: Preserves document structure, including headings, tables, and lists
- **Table Extraction**: Accurately extracts tabular data
- **Image Recognition**: Understands images and scanned documents
- **Markdown Export**: Converts documents to well-structured Markdown
- **Multi-format Support**: Handles PDFs, images (PNG, JPG, etc.), and more

## Installation

Install Dockling with the project dependencies:

```bash
pip install -r requirements.txt
```

Or install Dockling separately:

```bash
pip install docling docling-core pillow
```

## Usage

### 1. **Automatic Usage (Recommended)**

The system automatically uses Dockling when available:

```python
from src.data_loader import load_all_documents

# Automatically uses Dockling for better document understanding
documents = load_all_documents("data/", use_dockling=True)

# Or disable Dockling and use standard loaders
documents = load_all_documents("data/", use_dockling=False)
```

### 2. **Direct Dockling Usage**

```python
from src.dockling_loader import DocklingDocumentLoader

loader = DocklingDocumentLoader()

# Load a PDF with enhanced understanding
pdf_docs = loader.load_pdf_with_dockling("data/pdf/document.pdf")

# Load an image document
image_docs = loader.load_image_with_dockling("data/images/scan.png")

# Load all documents from a directory
all_docs = loader.load_all_documents_from_directory("data/")
```

### 3. **Analyze Documents**

Use the utility functions to analyze and extract structured content:

```python
from src.dockling_utils import analyze_document_with_dockling, extract_tables_from_document

# Analyze a document
analysis = analyze_document_with_dockling("data/pdf/report.pdf")
print(analysis["content"])  # Markdown content
print(analysis["tables"])   # Extracted tables
print(analysis["figures"])  # Extracted figures

# Extract tables only
tables = extract_tables_from_document("data/pdf/report.pdf")
for table in tables:
    print(table["content"])
```

## How RAGSearch Uses Dockling

The `RAGSearch` class now supports Dockling:

```python
from src.search import RAGSearch

# Use Dockling for better document understanding (default)
rag = RAGSearch(use_dockling=True)

# Or use standard loaders
rag = RAGSearch(use_dockling=False)

# Query as usual
result = rag.search_and_summarize("Your question here")
```

## Supported File Formats

### Dockling Formats (Enhanced):
- **PDF** - Professional documents, reports, papers
- **Images** - PNG, JPG, JPEG, BMP, TIFF (scanned documents)

### Standard Loader Formats:
- **CSV** - Comma-separated values
- **XLSX** - Excel spreadsheets
- **DOCX** - Microsoft Word documents
- **JSON** - JSON files
- **TXT** - Plain text files

## Example: Processing Documents with Dockling

```bash
# Analyze a PDF
python src/dockling_utils.py data/pdf/document.pdf
```

This will output:
- Document title
- Content length
- Number of tables and figures
- First 500 characters of extracted content

## Performance Tips

1. **First Run**: Building the FAISS index with Dockling takes longer due to enhanced extraction
2. **Subsequent Runs**: The index is cached, so queries are fast
3. **Memory**: Dockling uses more memory than standard loaders but provides better quality
4. **Disable if Needed**: If running on low-memory systems, set `use_dockling=False`

## Troubleshooting

### "Dockling not installed"
```bash
pip install dockling docling-core
```

### "Dockling not available, falling back to standard loaders"
This is normal. Dockling will fall back to standard loaders if not installed.

### PDF extraction is slow
- Large PDFs take longer to process
- This is normal and happens only on first index build
- Subsequent queries use the cached index

## Structured Content Output

Dockling exports content as Markdown, which preserves:
- **Headings**: `# H1`, `## H2`, etc.
- **Lists**: Bullets and numbered lists
- **Tables**: Formatted as Markdown tables
- **Code Blocks**: Preserved with syntax highlighting
- **Links**: Extracted hyperlinks

This structured format is excellent for RAG systems as it maintains context better than plain text.

## Next Steps

1. **Add PDFs**: Place your documents in `data/pdf/`
2. **Rebuild Index**: Delete `faiss_store/` to force a rebuild with Dockling
3. **Query**: Use the Streamlit app or RAGSearch API to query your documents

## Learn More

- [Dockling Documentation](https://github.com/DS4SD/docling)
- [Docling Models](https://huggingface.co/collections/ds4sd)
- [LangChain Integration](https://python.langchain.com/)
