"""Entry point for the Streamlit web application.

This module defines a simple user interface that allows users to upload
documents, preview the extracted text and obtain a summary via Gemini 2.5
Flash.  The UI validates file size and type, displays informative error
messages and exposes a button to trigger the LLM summarisation.
"""

import sys
import os
import streamlit as st
sys.path.append(os.path.dirname(__file__))
from ocr_utils import extract_text
from llm_utils import summarize_text



def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(page_title="Multimodal Document Analyzer", layout="wide")
    st.title("📄 Multimodal Document Analyzer")
    st.markdown(
        "Upload a PDF, DOCX, JPEG or PNG file.  The application will extract "
        "the text and then summarise it using the Gemini 2.5 Flash model."
    )

    uploaded_file = st.file_uploader(
        "Choose a file", type=["pdf", "docx", "jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        # Limit file size to 10 MB
        max_size = 10 * 1024 * 1024
        if len(file_bytes) > max_size:
            st.error("File exceeds maximum allowed size of 10 MB.")
            return

        # Extract text
        with st.spinner("Extracting text…"):
            try:
                text = extract_text(file_bytes, filename)
            except Exception as ex:
                st.error(f"Error extracting text: {ex}")
                return

        # Display extracted text in an expandable area
        with st.expander("Extracted Text", expanded=False):
            st.text_area("Document content", text, height=250)

        # Button to trigger summarisation
        if st.button("Summarize Document"):
            with st.spinner("Generating summary…"):
                try:
                    summary = summarize_text(text)
                    print(f"Summary result: {summary!r}")  # Print for server-side logs
                    st.subheader("Summary")
                    if summary:
                        st.write(summary)
                    else:
                        st.warning("No summary was generated. Please check your Gemini API key or try with another document.")
                except Exception as ex:
                    st.error(f"Error during summarisation: {ex}")



if __name__ == "__main__":
    main()