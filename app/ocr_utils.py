"""Utilities for extracting text from various document formats.

This module centralises the OCR logic used by the Streamlit application.  It
supports images (JPEG/PNG), PDFs and DOCX files.  PDFs are handled first
with `pdfplumber`, which extracts embedded text directly.  If no text is
returned for a page (e.g. a scanned document), the page is converted to an
image and passed to Tesseract OCR.  DOCX files are read using
`python-docx`/`docx2txt`.  Images are passed directly to Tesseract.  The
functions return a string containing all extracted text.
"""

from __future__ import annotations

import io
import os
import tempfile
from typing import List

from PIL import Image
import pytesseract
import pdfplumber
import docx2txt

pytesseract.pytesseract.tesseract_cmd = r'PATH_TO_tesseract.exe'

try:
    from pdf2image import convert_from_bytes
    _PDF2IMAGE_AVAILABLE = True
except ImportError:
    # pdf2image is an optional dependency; fallback to plain OCR only when
    # text extraction fails.
    _PDF2IMAGE_AVAILABLE = False


def _ocr_image(image: Image.Image, lang: str | None = None) -> str:
    """Run Tesseract OCR on a PIL Image.

    Parameters
    ----------
    image : PIL.Image.Image
        The image to process.
    lang : str, optional
        Language code for Tesseract (e.g. ``'eng'``).  If ``None`` the
        default language installed with Tesseract is used.

    Returns
    -------
    str
        The recognised text.
    """
    config = ""
    if lang:
        config += f" -l {lang}"
    return pytesseract.image_to_string(image, config=config)


def _extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """Extract text from a PDF using pdfplumber and optional OCR fallback.

    This function first attempts to extract text from each page using
    ``pdfplumber``.  If a page returns ``None`` or an empty string, it will
    attempt to run OCR on that page provided ``pdf2image`` is installed.

    Parameters
    ----------
    file_bytes : bytes
        The raw bytes of the PDF file.

    Returns
    -------
    str
        The concatenated text from all pages.
    """
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page_num, page in enumerate(pdf.pages):
            page_text = page.extract_text() or ""
            # If pdfplumber returns no text we fall back to OCR
            if page_text.strip() == "" and _PDF2IMAGE_AVAILABLE:
                # Convert just this page to an image
                images: List[Image.Image] = convert_from_bytes(
                    file_bytes, first_page=page_num + 1, last_page=page_num + 1
                )
                for img in images:
                    page_text += _ocr_image(img)
            text += page_text + "\n"
    return text


def extract_text(file_bytes: bytes, filename: str, *, lang: str | None = None) -> str:
    """Determine the file type and extract its text accordingly.

    Parameters
    ----------
    file_bytes : bytes
        The raw bytes of the uploaded file.
    filename : str
        The name of the file (used to infer the extension).
    lang : str, optional
        Language code to pass to Tesseract for OCR.  Default is ``None`` (let
        Tesseract use its default language).

    Returns
    -------
    str
        The extracted text.  Raises ``ValueError`` if the file format is
        unsupported.
    """
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext in {".png", ".jpg", ".jpeg"}:
        # Direct image OCR
        image = Image.open(io.BytesIO(file_bytes))
        return _ocr_image(image, lang=lang)
    elif ext == ".pdf":
        return _extract_text_from_pdf_bytes(file_bytes)
    elif ext == ".docx":
        # Write to a temporary file because docx2txt expects a file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file_bytes)
            tmp.flush()
            text = docx2txt.process(tmp.name)
        return text
    else:
        # As a last resort, try to decode as UTF‑8 text; if that fails, raise
        try:
            return file_bytes.decode("utf-8")
        except Exception:
            raise ValueError(f"Unsupported file format: {ext}")