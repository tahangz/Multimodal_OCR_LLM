"""
Multimodal OCR & LLM project
----------------------------

This package contains the modules necessary to build a Streamlit application
that extracts text from uploaded documents using OCR and summarises it using
Google's Gemini 2.5 Flash model.  See `README.md` for usage details.
"""

# Allow app modules to be imported as a package
__all__ = ["main", "ocr_utils", "llm_utils"]