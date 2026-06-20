<<<<<<< HEAD
# Literature Markdown Converter
=======
# 📚 Any File To Markdown Converter
>>>>>>> bf74be1fdef6ee3b4f969ac328f56d000f9a1c7a

Literature Markdown Converter is a professional, high-performance web application built with Streamlit and Python. It is designed to parse and convert various document formats—including scientific papers, slide presentations, spreadsheets, tabular data, and raw text files—into clean, standardized Markdown (.md) documents.

The application features a responsive, Neo-Brutalist design, support for single-file and batch-file uploads, recursive ZIP archive extraction, and secure local directory scanning.

---

## Features

* **Neo-Brutalist User Interface**: Custom styled layout utilizing modern typography (Space Grotesk and Space Mono) from Google Fonts, sharp styling elements, high-contrast borders, flat dropshadows, and a clean, responsive layout.
* **Flexible Input Methods**:
  * **Browser Upload**: Drag and drop or browse to upload individual documents or multiple files simultaneously. Supports ZIP archives; the app recursively unzips, processes files, and rebuilds directories in the output ZIP.
  * **Local Directory Scanning**: Input a directory path to scan the folder structure for supported documents. Detected documents are displayed in an interactive checkable table for customizable batch selection.
* **Real-Time Conversion Pipeline**: Visual feedback displays progress details, listing the currently processing document, file index, page-by-page progress for PDFs, and slide outlines for PPTX files.
* **Unified Output Download**: Export results as a single converted Markdown file or, for batch runs, a structured ZIP file preserving the input's relative folder structure.
* **Security Constraints**: Built-in safeguards validate local directories to prevent folder traversal. The app blocks folder scans on system roots (such as `C:\` or `D:\`) and operating system directories (like Windows, Program Files, `/usr`, `/etc`, and `/var`).

---

## Supported Formats and Parsers

The conversion pipeline integrates specific libraries to extract content structured for Markdown layout:

| Format | Extension | Parser Library | Extraction Behavior |
| :--- | :--- | :--- | :--- |
| **PDF** | `.pdf` | `PyPDF2` | Extracts text layout page-by-page, adding page headers (`## Page X`). |
| **Word** | `.docx` | `python-docx` | Traverses XML elements in exact visual order. Maps header styles to heading levels (`#`, `##`, etc.), retains bulleted and numbered lists, and structures tables as Markdown grids. |
| **PowerPoint** | `.pptx` | `python-pptx` | Extracts slide outlines. Outlines titles and handles indentation offsets for hierarchical bullets. |
| **Excel** | `.xlsx`, `.xls` | `pandas` + `openpyxl` | Translates each spreadsheet tab into a structured Markdown table grid. |
| **CSV** | `.csv` | `pandas` | Formats data tables directly to Markdown tables. |
| **Text** | `.txt` | Native Python I/O | Decodes text contents using UTF-8 with fallback replacement handling. |
| **Archive** | `.zip` | `zipfile` | Unpacks, filters, parses files recursively, and archives converted results. |

---

## Getting Started

### Prerequisites

Ensure you have Python 3.8 or higher installed on your system.

### Installation

1. Clone or download this repository.
2. Open your terminal, navigate to the project directory, and install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

Launch the Streamlit web application with:

```bash
streamlit run app.py
```

The application will run locally and automatically open in your default browser at `http://localhost:8501`.

---

## Project Structure

* **app.py**: Handles Streamlit frontend layouts, Neo-Brutalist CSS styles, user inputs, safety checks, interactive tables, and file download mechanisms.
* **converter.py**: Houses the core document parser classes, file-routing functions, recursive ZIP handling, and extraction logic.
* **requirements.txt**: Specifies the exact dependencies and versions required by the pipeline.
