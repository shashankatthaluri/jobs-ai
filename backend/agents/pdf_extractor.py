"""Agent 1: PDF Text Extraction.

Extracts raw text from PDF resume files.
No summarization, no cleanup beyond obvious headers/footers.
"""
import fitz  # PyMuPDF


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract all readable text from a PDF file.
    
    Args:
        file_bytes: Raw PDF file bytes
        
    Returns:
        Plain text extracted from the PDF, preserving order.
        
    Raises:
        ValueError: If PDF cannot be parsed
    """
    try:
        # Open PDF from bytes
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        
        text_blocks = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract text with layout preservation
            text = page.get_text("text")
            
            if text.strip():
                text_blocks.append(text)
        
        doc.close()
        
        # Join all pages
        full_text = "\n\n".join(text_blocks)
        
        # Basic cleanup - remove excessive whitespace
        lines = []
        for line in full_text.split("\n"):
            stripped = line.strip()
            if stripped:
                lines.append(stripped)
        
        return "\n".join(lines)
        
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")


def extract_text_from_pdf_with_blocks(file_bytes: bytes) -> str:
    """
    Extract text using block-based extraction for better structure.
    
    This method preserves document structure better for complex layouts.
    """
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        
        all_text = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get text blocks with position info
            blocks = page.get_text("blocks")
            
            # Sort blocks by position (top to bottom, left to right)
            sorted_blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
            
            for block in sorted_blocks:
                if block[6] == 0:  # Text block (not image)
                    text = block[4].strip()
                    if text:
                        all_text.append(text)
        
        doc.close()
        
        return "\n".join(all_text)
        
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")
