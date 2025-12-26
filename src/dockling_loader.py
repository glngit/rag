"""
Enhanced document loader using Dockling for superior document understanding.
Dockling provides better extraction of text, tables, and structured content from PDFs and images.
"""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from langchain.schema import Document
import logging

logger = logging.getLogger(__name__)


class DocklingDocumentLoader:
    """
    Document loader using Dockling for enhanced PDF and document understanding.
    Supports PDFs, images, and other document formats with better layout understanding.
    """
    
    def __init__(self):
        """Initialize Dockling loader"""
        try:
            from docling.document_converter import DocumentConverter
            self.converter = DocumentConverter()
            self.dockling_available = True
            logger.info("[INFO] Dockling initialized successfully")
        except ImportError:
            logger.warning("[WARNING] Dockling not available, will fall back to standard loaders")
            self.dockling_available = False
            self.converter = None
    
    def load_pdf_with_dockling(self, file_path: str) -> List[Document]:
        """
        Load PDF file using Dockling with advanced document understanding.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of LangChain Document objects with enhanced content
        """
        if not self.dockling_available:
            logger.warning(f"[WARNING] Dockling not available for {file_path}, using fallback")
            return self._fallback_pdf_loader(file_path)
        
        try:
            logger.info(f"[INFO] Loading PDF with Dockling: {file_path}")
            
            # Convert document using Dockling
            result = self.converter.convert(file_path)
            
            documents = []
            
            # Extract structured content
            if result.document:
                # Get markdown representation with preserved structure
                markdown_content = result.document.export_to_markdown()
                
                # Create document with metadata
                doc = Document(
                    page_content=markdown_content,
                    metadata={
                        "source": file_path,
                        "loader": "dockling",
                        "format": "markdown",
                        "title": Path(file_path).stem,
                    }
                )
                documents.append(doc)
                
                logger.info(f"[INFO] Successfully loaded PDF with Dockling: {file_path}")
            
            return documents
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to load PDF with Dockling: {e}")
            return self._fallback_pdf_loader(file_path)
    
    def load_image_with_dockling(self, file_path: str) -> List[Document]:
        """
        Load image file (PNG, JPG, etc.) using Dockling's document understanding.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            List of LangChain Document objects
        """
        if not self.dockling_available:
            logger.warning(f"[WARNING] Dockling not available for image {file_path}")
            return []
        
        try:
            logger.info(f"[INFO] Loading image with Dockling: {file_path}")
            
            result = self.converter.convert(file_path)
            documents = []
            
            if result.document:
                markdown_content = result.document.export_to_markdown()
                
                doc = Document(
                    page_content=markdown_content,
                    metadata={
                        "source": file_path,
                        "loader": "dockling",
                        "format": "image",
                        "title": Path(file_path).stem,
                    }
                )
                documents.append(doc)
                
                logger.info(f"[INFO] Successfully loaded image with Dockling: {file_path}")
            
            return documents
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to load image with Dockling: {e}")
            return []
    
    def _fallback_pdf_loader(self, file_path: str) -> List[Document]:
        """
        Fallback PDF loader using PyPDF when Dockling is unavailable.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            List of LangChain Document objects
        """
        try:
            from langchain_community.document_loaders import PyPDFLoader
            
            logger.info(f"[INFO] Using fallback PyPDF loader for: {file_path}")
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            # Enhance metadata
            for doc in documents:
                doc.metadata["loader"] = "pypdf"
                doc.metadata["title"] = Path(file_path).stem
            
            return documents
            
        except Exception as e:
            logger.error(f"[ERROR] Fallback PDF loader failed: {e}")
            return []
    
    def load_document(self, file_path: str) -> List[Document]:
        """
        Load any supported document format automatically.
        Detects file type and uses appropriate loader.
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of LangChain Document objects
        """
        file_path = str(file_path)
        file_ext = Path(file_path).suffix.lower()
        
        logger.info(f"[INFO] Loading document: {file_path} (type: {file_ext})")
        
        # PDF and image formats - use Dockling if available
        if file_ext in ['.pdf']:
            return self.load_pdf_with_dockling(file_path)
        
        elif file_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            return self.load_image_with_dockling(file_path)
        
        # Other formats - use standard loaders
        else:
            return self._load_standard_document(file_path)
    
    def _load_standard_document(self, file_path: str) -> List[Document]:
        """
        Load documents using standard LangChain loaders.
        
        Args:
            file_path: Path to the document
            
        Returns:
            List of LangChain Document objects
        """
        file_ext = Path(file_path).suffix.lower()
        
        try:
            if file_ext == '.txt':
                from langchain_community.document_loaders import TextLoader
                loader = TextLoader(file_path)
                
            elif file_ext == '.csv':
                from langchain_community.document_loaders import CSVLoader
                loader = CSVLoader(file_path)
                
            elif file_ext == '.xlsx':
                from langchain_community.document_loaders.excel import UnstructuredExcelLoader
                loader = UnstructuredExcelLoader(file_path)
                
            elif file_ext == '.docx':
                from langchain_community.document_loaders import Docx2txtLoader
                loader = Docx2txtLoader(file_path)
                
            elif file_ext == '.json':
                from langchain_community.document_loaders import JSONLoader
                loader = JSONLoader(file_path)
                
            else:
                logger.warning(f"[WARNING] Unsupported file format: {file_ext}")
                return []
            
            documents = loader.load()
            
            # Enhance metadata
            for doc in documents:
                doc.metadata["title"] = Path(file_path).stem
                doc.metadata["source"] = file_path
            
            logger.info(f"[INFO] Loaded {len(documents)} documents from {file_path}")
            return documents
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to load {file_path}: {e}")
            return []
    
    def load_all_documents_from_directory(self, data_dir: str) -> List[Document]:
        """
        Load all supported documents from a directory recursively.
        
        Args:
            data_dir: Directory containing documents
            
        Returns:
            List of all loaded documents
        """
        data_path = Path(data_dir).resolve()
        logger.info(f"[INFO] Loading all documents from: {data_path}")
        
        all_documents = []
        
        # Support various file extensions
        supported_extensions = [
            '*.pdf', '*.txt', '*.csv', '*.xlsx', '*.docx', '*.json',
            '*.png', '*.jpg', '*.jpeg', '*.bmp', '*.tiff'
        ]
        
        for extension in supported_extensions:
            for file_path in data_path.glob(f'**/{extension}'):
                try:
                    documents = self.load_document(str(file_path))
                    all_documents.extend(documents)
                except Exception as e:
                    logger.error(f"[ERROR] Failed to process {file_path}: {e}")
        
        logger.info(f"[INFO] Total documents loaded: {len(all_documents)}")
        return all_documents


# Convenience function
def load_documents_with_dockling(data_dir: str) -> List[Document]:
    """
    Load all documents from a directory using Dockling-enhanced loading.
    
    Args:
        data_dir: Directory containing documents
        
    Returns:
        List of LangChain Document objects
    """
    loader = DocklingDocumentLoader()
    return loader.load_all_documents_from_directory(data_dir)
