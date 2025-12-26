"""
Example usage of Dockling for document understanding.
Demonstrates how to extract tables, figures, and structured content from documents.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def analyze_document_with_dockling(file_path: str) -> Dict[str, Any]:
    """
    Analyze a document using Dockling and extract structured content.
    
    Args:
        file_path: Path to the document (PDF, image, etc.)
        
    Returns:
        Dictionary with document analysis results
    """
    try:
        from docling.document_converter import DocumentConverter
        from docling.document_converter import DocumentConverter
        
        converter = DocumentConverter()
        result = converter.convert(file_path)
        
        analysis = {
            "source": file_path,
            "title": Path(file_path).stem,
            "content": None,
            "tables": [],
            "figures": [],
            "metadata": {}
        }
        
        if result.document:
            # Extract markdown content with preserved structure
            analysis["content"] = result.document.export_to_markdown()
            
            # Extract tables if available
            if hasattr(result.document, 'tables'):
                analysis["tables"] = result.document.tables
            
            # Extract figures if available
            if hasattr(result.document, 'figures'):
                analysis["figures"] = result.document.figures
            
            # Store document metadata
            if hasattr(result.document, 'metadata'):
                analysis["metadata"] = result.document.metadata
        
        logger.info(f"[INFO] Successfully analyzed document: {file_path}")
        return analysis
        
    except ImportError:
        logger.error("[ERROR] Dockling not installed. Install with: pip install docling docling-core")
        return {"error": "Dockling not available"}
    except Exception as e:
        logger.error(f"[ERROR] Failed to analyze document: {e}")
        return {"error": str(e)}


def extract_tables_from_document(file_path: str) -> List[Dict[str, Any]]:
    """
    Extract all tables from a document.
    
    Args:
        file_path: Path to the document
        
    Returns:
        List of extracted tables with content
    """
    try:
        from docling.document_converter import DocumentConverter
        
        converter = DocumentConverter()
        result = converter.convert(file_path)
        
        tables = []
        
        if result.document:
            # Iterate through document elements and extract tables
            for element in result.document.elements:
                if hasattr(element, '__class__') and 'Table' in element.__class__.__name__:
                    table_data = {
                        "type": "table",
                        "content": str(element),
                        "source": file_path
                    }
                    tables.append(table_data)
        
        logger.info(f"[INFO] Extracted {len(tables)} tables from {file_path}")
        return tables
        
    except ImportError:
        logger.error("[ERROR] Dockling not installed")
        return []
    except Exception as e:
        logger.error(f"[ERROR] Failed to extract tables: {e}")
        return []


def chunk_markdown_content(markdown_content: str, chunk_size: int = 500, chunk_overlap: int = 100) -> List[str]:
    """
    Split Dockling-extracted markdown content into chunks.
    Preserves structure and headings for better context.
    
    Args:
        markdown_content: Markdown content from Dockling
        chunk_size: Target chunk size in characters
        chunk_overlap: Number of overlapping characters between chunks
        
    Returns:
        List of content chunks
    """
    chunks = []
    
    # Split by major sections (###) first to preserve structure
    sections = markdown_content.split('\n###')
    
    for section in sections:
        # Add back the ### for all but the first section
        if sections.index(section) > 0:
            section = '###' + section
        
        # If section is small enough, add as-is
        if len(section) <= chunk_size:
            chunks.append(section)
        else:
            # Split larger sections into chunks with overlap
            start = 0
            while start < len(section):
                end = min(start + chunk_size, len(section))
                chunk = section[start:end]
                chunks.append(chunk)
                start = end - chunk_overlap
    
    logger.info(f"[INFO] Split content into {len(chunks)} chunks")
    return chunks


# Example usage
if __name__ == "__main__":
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        
        # Analyze document
        print(f"\n{'='*50}")
        print(f"Analyzing: {pdf_path}")
        print(f"{'='*50}\n")
        
        analysis = analyze_document_with_dockling(pdf_path)
        
        if "error" not in analysis:
            print(f"Title: {analysis['title']}")
            print(f"Content length: {len(analysis['content'])} characters")
            print(f"Number of tables: {len(analysis['tables'])}")
            print(f"Number of figures: {len(analysis['figures'])}")
            
            # Display first 500 characters of content
            print(f"\nFirst 500 characters of content:")
            print("-" * 50)
            print(analysis['content'][:500])
            print("-" * 50)
        else:
            print(f"Error: {analysis['error']}")
    else:
        print("Usage: python dockling_utils.py <file_path>")
        print("Example: python dockling_utils.py data/pdf/document.pdf")
