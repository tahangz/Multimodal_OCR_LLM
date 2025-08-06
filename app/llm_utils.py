"""Wrapper functions for interacting with Gemini models via LangChain.

This module encapsulates the logic for communicating with Google’s Gemini
language models using LangChain’s `ChatGoogleGenerativeAI` interface.  It
expects a valid API key in the ``GOOGLE_API_KEY`` environment variable or
supplied via function parameters.  See the LangChain documentation for more
details on available parameters【369091272480127†L449-L456】.
"""

import os
from typing import Optional

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def _get_api_key(explicit_key : Optional[str] = None) -> str:
    """Return the Google API key from an explicit argument or environment.

    Parameters
    ----------
    explicit_key : str, optional
        API key provided directly by the caller.  If not provided, the
        ``GOOGLE_API_KEY`` environment variable is checked.

    Returns
    -------
    str
        The API key.  Raises ``ValueError`` if no key is available.
    """
    api_key = YOUR_API_KEY  or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "No Google API key provided.  Set the GOOGLE_API_KEY environment variable"
        )
    return api_key


def summarize_text(text: str, *, api_key: Optional[str] = None) -> str:
    """Generate a concise summary of the provided text using Gemini 2.5 Flash.

    This function constructs a LangChain `LLMChain` with a prompt template
    instructing the model to summarise the document.  It then invokes the
    chain and returns the resulting summary.

    Parameters
    ----------
    text : str
        The text to summarise.
    api_key : str, optional
        Explicit Google API key.  If not provided the key is read from the
        environment.

    Returns
    -------
    str
        The summary returned by the LLM.

    Raises
    ------
    ValueError
        If no API key is available.
    """
    key = _get_api_key(api_key)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=key,
        temperature=0.2,
        max_output_tokens=1024,
    )
    prompt = PromptTemplate(
        input_variables=["text"],
        template=(
            "You are a helpful assistant. Read the following document text extracted with OCR "
            "and provide a concise summary highlighting the main points. Be clear and coherent.\n\n"
            "Document text extracted with OCR :\n{text}\n\nSummary:"
        ),
    )
    # New chaining API: use the | operator to create a RunnableSequence
    chain = prompt | llm
    # The input must be a dict matching the prompt variables
    result = chain.invoke({"text": text})
    # The result from ChatGoogleGenerativeAI is an object with 'content'
    # If you want the plain string:
    print(f"LLM result: {result!r}")  # Print for server-side logs
    if hasattr(result, 'content'):
        return result.content
    elif isinstance(result, dict) and 'content' in result:
        return result['content']
    return str(result)