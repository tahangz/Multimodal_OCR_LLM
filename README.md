# Multimodal OCR & LLM Document Analyzer

This project demonstrates how to build a simple multimodal document analysis
application.  Users can upload PDFs, DOCX files or images (JPEG/PNG).  The
application extracts text using OCR when necessary and then summarizes the
content using Google's Gemini 2.5 Flash large language model.  A
Streamlit-based web interface makes it easy to use locally or deploy to the
cloud.

## Features

* **Multi‑format input** – Accepts images (`.png`, `.jpg`/`.jpeg`), PDFs and
  Microsoft Word (`.docx`) files.  Unsupported formats are rejected.
* **Text extraction** – Uses [`pytesseract`](https://pypi.org/project/pytesseract/)
  to perform optical character recognition on images and
  [`pdfplumber`](https://pypi.org/project/pdfplumber/) to extract embedded text from
  PDFs.  If a PDF page has no extractable text (for example, when it is a
  scanned image), the code falls back to OCR after converting the page to an
  image.
* **Summarisation with Gemini 2.5 Flash** – The
  [`langchain-google-genai`](https://python.langchain.com/api_reference/google_genai/)
  integration wraps Google’s Gemini models.  The
  `ChatGoogleGenerativeAI` class reads your API key either from the
  `GOOGLE_API_KEY` environment variable or via a `google_api_key` argument【369091272480127†L449-L456】.
  Once the key is configured the model can be invoked with a simple
  function call【65511366144955†L126-L146】.
* **Streamlit user interface** – A single page allows you to upload a file,
  view the extracted text and request a summary from the LLM.  Error cases
  (such as invalid files or OCR failures) are handled gracefully and reported
  to the user.

## Project structure

```
multimodal_ocr_llm_project/
├── app/                 # Python source code for the application
│   ├── __init__.py      # Marks the app as a Python package
│   ├── main.py          # Streamlit entry point
│   ├── ocr_utils.py     # OCR and text‑extraction helpers
│   └── llm_utils.py     # Wrapper around the Gemini API via LangChain
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container configuration for deployment
├── .env.example         # Template for environment variables
└── README.md            # You are here
```

## Getting started

### Prerequisites

* **Python 3.11** – Other recent Python 3 versions should also work.
* **Tesseract OCR** – On Linux you can install it with `sudo apt-get install tesseract-ocr`.
* A **Google Generative AI API key**.  Sign up through [Google AI Studio](https://makersuite.google.com/) and create
  an API key.  The key can be set in an environment variable named
  `GOOGLE_API_KEY` (preferred) or passed directly to the
  `ChatGoogleGenerativeAI` constructor【369091272480127†L449-L456】.

### Installation

1. Clone this repository or copy the `multimodal_ocr_llm_project` folder to your
   machine.
2. Ensure Tesseract is installed and available in your `PATH`.
3. Create a virtual environment and activate it:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   to deactivate :
   ```bash
   deactivate
   ```

4. Install the Python dependencies:

   ```bash
   python.exe -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. fill in your API key `.env` 

6. Run the Streamlit app:

   ```bash
   streamlit run app/main.py
   ```

   The web interface will open in your browser at <http://localhost:8501>.

### Usage

1. Navigate to the Streamlit page.
2. Upload a document (PDF, DOCX, JPEG or PNG).  The app will show the
   extracted text in a text area.
3. Click **“Summarize Document”** to send the extracted text to Gemini 2.5 Flash.
   The LLM summary will appear below the button.

### Deployment

#### Docker

To run the application inside a container, build the Docker image and start it
locally:

```bash
docker build -t multimodal-ocr-llm .
docker run -p 8501:8501 --env-file .env multimodal-ocr-llm
```

#### Azure App Service

1. Push the image to a container registry (Azure Container Registry or
   Docker Hub).
2. Create an **App Service** instance and configure it to pull the image.
3. Set the `GOOGLE_API_KEY` environment variable in the App Service
   configuration.
4. Expose port 8501.

Alternatively you can use Azure Web Apps for Containers.  If you prefer not
to use Docker, deploy the code to an Azure **App Service** or **Function** with
a custom runtime and ensure that Tesseract and other system dependencies are
available.

### Extending the project

* **Language support** – Tesseract supports many languages.  Change
  `pytesseract.image_to_string(image, lang="... ")` in `ocr_utils.py` to use a
  different language model.
* **Chunking** – For very large documents you may want to chunk the text and
  summarise each part individually.  LangChain’s `RecursiveCharacterTextSplitter`
  is a useful tool for this.
* **Additional models** – The `llm_utils.py` wrapper can be extended to use
  other models or providers (e.g. local LLaMA via Ollama or MistralAI) by
  swapping out the LangChain LLM class.
