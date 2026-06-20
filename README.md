# 📚 Literature Markdown Converter

A high-performance, premium web application built using **Streamlit** to convert scientific papers, slides, datasets, and text documents into standard, clean **Markdown (.md)** format. 

This tool supports processing both single files, multiple files, complete nested folder structures (uploaded via ZIP archives), and local directory scanning. It provides real-time progress details with a beautiful glassmorphic waiting animation.

---

## ✨ Features

- **🎨 Modern Visual Design:** Glassmorphism dashboard styled using custom CSS, custom Google typography ("Plus Jakarta Sans" and "JetBrains Mono"), glowing accents, and dynamic transitions.
- **📂 Flexible Input Formats:**
  - **Browser Mode:** Upload files directly or upload a ZIP archive of folders. The app recursively traverses zip subdirectories and preserves the structural hierarchy in the output zip!
  - **Local Scan Mode:** Enter an absolute directory path (e.g. `D:\Literature-MD-Converter\test_documents`). The application scans for matching files and displays them in an interactive checklist using `st.data_editor`.
- **⏳ Glowing Live Spinner Animation:** Real-time waiting state indicator showing the active file being parsed and page-by-page or slide-by-slide progress details.
- **🔍 Markdown Document Previewer:** View successfully converted files side-by-side:
  - **Rendered Document:** View Markdown headings, lists, tables, and spacing formatted live.
  - **Raw Markdown Source:** View raw text syntax in a scrollable, styled code box.
- **📥 Unified Export:** Download all parsed markdowns in a single click, packaged inside a ZIP folder maintaining the original relative layout.

---

## 🛠️ Supported Extensions & Parsers

| Format | Library Used | Parsing Behavior |
| :--- | :--- | :--- |
| **PDF (`.pdf`)** | `PyPDF2` | Extracts text layout page-by-page, adding header anchors (`## Page X`). |
| **Word (`.docx`)** | `python-docx` | Traverses XML elements in exact visual order. Maps heading styles to standard markdown blocks (`#`, `##`, etc.) and translates tables to Markdown table grids. |
| **PowerPoint (`.pptx`)**| `python-pptx` | Splits outlines slide-by-slide. Renders shapes in context, using text levels to indent sub-bullets. |
| **Excel (`.xlsx`, `.xls`)**| `pandas` + `openpyxl` | Converts multiple spreadsheet tabs into Markdown tables (`tabulate` engine). |
| **CSV (`.csv`)** | `pandas` | Formats data tables to markdown format. |
| **Text (`.txt`)** | Native I/O | Decodes UTF-8 text with fallback replacement handling. |
| **Archive (`.zip`)** | `zipfile` | Unzips and recursively runs parsers on nested files, rebuilding directories inside the final ZIP export. |

---

## 🚀 Getting Started

### 1. Prerequisites
Make sure you have Python 3.8+ installed.

### 2. Installation
Clone the repository, navigate to the folder, and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Launching the App
Run the Streamlit server:
```bash
streamlit run app.py
```

The web page will open automatically in your browser at `http://localhost:8501`.
