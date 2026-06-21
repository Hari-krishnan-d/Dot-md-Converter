import streamlit as st
import pandas as pd
import os
import html
import streamlit.components.v1 as components
from converter import run_conversion_pipeline

# Set page config with expanded sidebar by default
st.set_page_config(
    page_title="Any File to Markdown Converter",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Neo-Brutalist CSS Styling with Mobile Responsiveness
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700;900&family=Space+Mono:wght@400;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Space Grotesk', sans-serif;
    color: #1C1917; /* Pure black text */
    background-color: #FAF9F5; /* Warm off-white brutalist background */
}

/* Container Padding - Responsive */
[data-testid="stAppViewContainer"] {
    padding: 2rem 4rem;
    background-image: none;
}

@media (max-width: 992px) {
    [data-testid="stAppViewContainer"] {
        padding: 1.5rem 2rem;
    }
}
@media (max-width: 768px) {
    [data-testid="stAppViewContainer"] {
        padding: 1rem 1rem;
    }
}

/* Header style card */
.header-panel {
    background: #FFE600; /* Neon Yellow background */
    border: 4px solid #1C1917;
    border-radius: 0px; /* Sharp brutalist corners */
    padding: 35px 25px;
    margin-bottom: 35px;
    box-shadow: 6px 6px 0px #FF007F; /* Hot Pink flat shadow */
    text-align: left;
}

@media (max-width: 768px) {
    .header-panel {
        padding: 20px 15px;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 2.2rem !important;
        letter-spacing: -1px !important;
    }
    .header-subtitle {
        font-size: 1rem !important;
    }
}

.header-title {
    font-size: 3rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: -1.5px;
    color: #1C1917;
    margin-bottom: 8px;
    line-height: 1.1;
}

.header-subtitle {
    color: #1C1917;
    font-size: 1.15rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Dashboard Cards (White background, black borders, neon green flat shadow) */
.metric-card {
    background: #FFFFFF;
    border: 3px solid #1C1917;
    border-radius: 0px;
    padding: 20px;
    text-align: center;
    box-shadow: 5px 5px 0px #39FF14; /* Neon Green shadow */
    transition: all 0.15s ease;
}
.metric-card:hover {
    transform: translate(-2px, -2px);
    box-shadow: 7px 7px 0px #39FF14;
}
.metric-value {
    font-size: 2.2rem;
    font-weight: 900;
    color: #1C1917;
    margin-bottom: 5px;
    font-family: 'Space Mono', monospace;
}
.metric-label {
    font-size: 0.85rem;
    color: #1C1917;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

@media (max-width: 768px) {
    .metric-card {
        padding: 12px;
        margin-bottom: 12px;
    }
    .metric-value {
        font-size: 1.6rem;
    }
    .metric-label {
        font-size: 0.75rem;
    }
}

/* Custom Tab styling */
div[data-baseweb="tab-list"] {
    background-color: transparent !important;
    border-radius: 0px !important;
    padding: 0px !important;
    border: none !important;
    border-bottom: 4px solid #1C1917 !important; /* Thick black split line */
    margin-bottom: 25px;
}
button[data-baseweb="tab"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    border-radius: 0px !important;
    margin-right: 8px !important;
    padding: 12px 24px !important;
    background-color: #FFFFFF !important;
    color: #1C1917 !important;
    border: 3px solid #1C1917 !important;
    box-shadow: 2px 2px 0px #1C1917 !important;
    transition: all 0.1s ease !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #FF007F !important; /* Hot Pink selection */
    color: #FFFFFF !important;
    transform: translateY(-2px);
    box-shadow: 3px 3px 0px #39FF14 !important; /* Neon Green shadow */
}

@media (max-width: 768px) {
    button[data-baseweb="tab"] {
        padding: 10px 15px !important;
        font-size: 0.9rem !important;
        margin-right: 4px !important;
    }
}

/* Input elements styling */
div[data-testid="stTextInput"] input {
    background-color: #FFFFFF !important;
    border: 3px solid #1C1917 !important; /* Solid black border */
    border-radius: 0px !important;
    color: #1C1917 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    box-shadow: 3px 3px 0px #FF007F !important; /* Hot Pink shadow */
    padding: 10px 14px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #39FF14 !important; /* Neon Green focus */
}

/* File Uploader styling */
[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border: 3px dashed #1C1917 !important; /* Black dashed border */
    border-radius: 0px !important;
    padding: 30px !important;
    box-shadow: 4px 4px 0px #39FF14 !important; /* Neon Green shadow */
}

/* Ensure all text within file uploader is visible (black text on white background) */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] small {
    color: #1C1917 !important;
}

/* Style the file uploader Browse button */
[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"],
[data-testid="stFileUploader"] section button {
    background-color: #FFE600 !important; /* Neon Yellow */
    color: #1C1917 !important; /* Black text */
    border: 3px solid #1C1917 !important;
    border-radius: 0px !important;
    box-shadow: 3px 3px 0px #1C1917 !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    padding: 8px 16px !important;
    transition: all 0.1s ease !important;
}

[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"]:hover,
[data-testid="stFileUploader"] section button:hover {
    background-color: #E6CF00 !important;
    transform: translate(-1px, -1px);
    box-shadow: 4px 4px 0px #1C1917 !important;
}

[data-testid="stFileUploader"] button[data-testid="baseButton-secondary"]:active,
[data-testid="stFileUploader"] section button:active {
    transform: translate(1px, 1px);
    box-shadow: 2px 2px 0px #1C1917 !important;
}

@media (max-width: 768px) {
    [data-testid="stFileUploader"] {
        padding: 15px !important;
    }
}

/* Waiting animation spinner */
.loader-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 30px;
    background: #FFFFFF;
    border: 4px solid #1C1917; /* Solid Black */
    border-radius: 0px;
    box-shadow: 6px 6px 0px #39FF14; /* Neon Green shadow */
    margin: 25px 0;
}
.spinner {
    position: relative;
    width: 60px;
    height: 60px;
    border: 6px solid #F3F4F6;
    border-top-color: #39FF14; /* Neon Green */
    border-right-color: #FF007F; /* Hot Pink */
    border-radius: 0%; /* Sharp square spinner */
    animation: spin 0.8s linear infinite;
    box-shadow: 0 0 10px rgba(57, 255, 20, 0.2);
}
.loader-text {
    font-size: 1.4rem;
    font-weight: 900;
    color: #1C1917;
    margin-top: 20px;
    text-transform: uppercase;
    letter-spacing: -0.5px;
}
.loader-subtext {
    font-size: 1rem;
    color: #374151;
    margin-top: 8px;
    font-family: 'Space Mono', monospace;
    font-weight: 500;
    text-align: center;
}
.active-file {
    color: #FF007F; /* Hot Pink */
    font-weight: 700;
}
.loader-detail {
    font-size: 0.85rem;
    color: #39FF14; /* Neon Green text */
    background: #1C1917; /* Pure black wrapper */
    padding: 4px 8px;
    margin-top: 8px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: center;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Primary actions: Convert button */
div.stButton > button:first-child {
    background: #39FF14 !important; /* Neon Green */
    color: #000000 !important; /* Pure Black text */
    border: 3px solid #1C1917 !important;
    border-radius: 0px !important;
    padding: 14px 32px !important;
    font-size: 1.1rem !important;
    font-weight: 900 !important;
    text-transform: uppercase;
    box-shadow: 4px 4px 0px #FF007F !important; /* Hot Pink shadow */
    transition: all 0.1s ease !important;
    width: 100% !important;
}
div.stButton > button:first-child:hover {
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0px #FF007F !important;
    background-color: #32E010 !important;
}
div.stButton > button:first-child:active {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0px #FF007F !important;
}

/* Custom Neo-Brutalist Download Button Styling */
div.stDownloadButton > button, div[data-testid="stDownloadButton"] > button {
    background: #FF007F !important; /* Hot Pink */
    color: #FFFFFF !important; /* Pure White text */
    border: 3px solid #1C1917 !important;
    border-radius: 0px !important;
    padding: 14px 32px !important;
    font-size: 1.15rem !important;
    font-weight: 900 !important;
    text-transform: uppercase;
    box-shadow: 4px 4px 0px #39FF14 !important; /* Neon Green shadow */
    transition: all 0.1s ease !important;
    width: 100% !important;
}
div.stDownloadButton > button:hover, div[data-testid="stDownloadButton"] > button:hover {
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0px #39FF14 !important;
    background-color: #E60072 !important;
}
div.stDownloadButton > button:active, div[data-testid="stDownloadButton"] > button:active {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0px #39FF14 !important;
}

/* Secondary Button overrides (Reset button, directory scan button) */
div.stButton > button:not(:first-child) {
    background: #FF007F !important; /* Hot Pink */
    color: #FFFFFF !important;
    border: 3px solid #1C1917 !important;
    border-radius: 0px !important;
    font-weight: 800 !important;
    text-transform: uppercase;
    box-shadow: 3px 3px 0px #39FF14 !important; /* Neon Green shadow */
    transition: all 0.1s ease !important;
}
div.stButton > button:not(:first-child):hover {
    transform: translate(-1px, -1px);
    box-shadow: 4px 4px 0px #39FF14 !important;
    background-color: #E60072 !important;
}

/* Sidebar styling override - Explicit visibility controls */
[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 3px solid #1C1917 !important;
}
[data-testid="stSidebar"], 
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] span, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] .stMarkdown {
    color: #1C1917 !important; /* Force all text to black */
}
[data-testid="stSidebar"] div[data-testid="stNotification"] {
    background-color: #FAF9F5 !important;
    border: 2px solid #1C1917 !important;
    border-radius: 0px !important;
}
[data-testid="stSidebar"] div[data-testid="stNotification"] * {
    color: #1C1917 !important;
}

/* Checkbox and table styling overrides */
div[data-testid="stTable"] table {
    border-collapse: collapse;
}
div[data-testid="stTable"] th {
    background-color: #FFE600 !important; /* Neon Yellow */
    color: #1C1917 !important;
    border: 2px solid #1C1917 !important;
    font-weight: 700;
}
div[data-testid="stTable"] td {
    background-color: #FFFFFF !important;
    color: #1C1917 !important;
    border: 2px solid #1C1917 !important;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
::-webkit-scrollbar-track {
    background: #FAF9F5;
}
::-webkit-scrollbar-thumb {
    background: #1C1917;
    border-radius: 0px;
    border: 2px solid #FAF9F5;
}
::-webkit-scrollbar-thumb:hover {
    background: #FF007F; /* Hot Pink */
}
</style>
""", unsafe_allow_html=True)


def show_loading_spinner(file_name, progress_detail=""):
    """Render square rotating Neo-Brutalist loading animation."""
    html_content = f"""
    <div class="loader-container">
        <div class="spinner"></div>
        <div class="loader-text">Converting Document</div>
        <div class="loader-subtext">Processing: <span class="active-file">{html.escape(file_name)}</span></div>
        <div class="loader-detail">{html.escape(progress_detail)}</div>
    </div>
    """
    return html_content


def is_safe_local_path(target_path):
    """Vulnerability Prevention: Block system roots and directory traversals."""
    resolved_path = os.path.abspath(target_path)
    
    # 1. Block drive root folders (like C:\, D:\, /)
    root_paths = [os.path.abspath(f"{d}:\\") for d in "abcdefghijklmnopqrstuvwxyz"] + [os.path.abspath("/")]
    if resolved_path in root_paths:
        return False
        
    # 2. Block operating system directory paths
    system_paths = [
        "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", "C:\\Users",
        "/etc", "/var", "/usr", "/sys", "/proc", "/boot", "/bin", "/sbin"
    ]
    for sys_dir in system_paths:
        if resolved_path.startswith(os.path.abspath(sys_dir)):
            return False
            
    return True


# Main Title Card
st.markdown("""
<div class="header-panel">
    <div class="header-title">Literature MD Converter</div>
    <div class="header-subtitle">Batch convert PDF, Word, PowerPoint, Excel sheets, and CSV documents to clean Markdown.</div>
</div>
""", unsafe_allow_html=True)

# State initialization
if "conversion_done" not in st.session_state:
    st.session_state.conversion_done = False
    st.session_state.converted_zip = None
    st.session_state.converted_results = None
    st.session_state.conversion_time = 0.0
    st.session_state.is_single_output = False
    st.session_state.single_file_name = ""
    st.session_state.single_file_content = ""

if "scanned_files" not in st.session_state:
    st.session_state.scanned_files = None
    st.session_state.scanned_path = ""

# Widget dynamic key counters to clear widgets on reset
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "local_path_key" not in st.session_state:
    st.session_state.local_path_key = 0

# Sidebar settings & info
with st.sidebar:
    st.markdown("### 📚 Supported Formats")
    st.info("""
    - **PDF:** Text extracted page-by-page.
    - **DOCX:** Style headers mapped, lists kept, tables parsed.
    - **PPTX:** Structured slide-by-slide lists.
    - **CSV & Excel:** Auto-rendered to neat markdown tables.
    - **ZIP / Directories:** Parsed recursively, folder path preserved.
    """)
    st.markdown("---")
    if st.button("🔄 Reset App"):
        # Increment uploader and path keys to force a brand new initialization, clearing browser caches
        st.session_state.uploader_key += 1
        st.session_state.local_path_key += 1
        st.session_state.scanned_files = None
        st.session_state.scanned_path = ""
        st.session_state.conversion_done = False
        st.session_state.converted_zip = None
        st.session_state.converted_results = None
        st.session_state.is_single_output = False
        st.session_state.single_file_name = ""
        st.session_state.single_file_content = ""
        st.rerun()

# Source modes tabs
tabs = st.tabs(["📤 Browser Upload (Files/ZIPs)", "📂 Local Directory Scan"])

files_to_process = []
source_mode = "browser"

with tabs[0]:
    st.markdown("##### Select Documents or ZIP Archives:")
    uploaded_files = st.file_uploader(
        "Upload files directly",
        type=["pdf", "docx", "pptx", "csv", "xlsx", "xls", "txt", "zip"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key=f"uploader_{st.session_state.uploader_key}"
    )
    
    if uploaded_files:
        st.write(f"📂 Selected **{len(uploaded_files)}** item(s) for conversion.")
        for u in uploaded_files:
            files_to_process.append({
                "name": u.name,
                "bytes": u.getvalue(),
                "is_zip": u.name.lower().endswith(".zip")
            })

with tabs[1]:
    st.markdown("##### Enter Path to Directory:")
    local_path = st.text_input(
        "Directory Path input",
        placeholder="e.g. D:\\Literature-MD-Converter\\test_documents",
        label_visibility="collapsed",
        key=f"local_path_{st.session_state.local_path_key}"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔍 Scan Directory"):
            if not local_path.strip():
                st.error("Please enter a directory path.")
            elif not os.path.exists(local_path):
                st.error("The specified path does not exist.")
            elif not os.path.isdir(local_path):
                st.error("The specified path is a file.")
            elif not is_safe_local_path(local_path):
                st.error("Security Warning: Scans are restricted from root drives and system OS directories.")
            else:
                supported = (".pdf", ".docx", ".pptx", ".csv", ".xlsx", ".xls", ".txt", ".zip")
                found_files = []
                for root, dirs, files in os.walk(local_path):
                    for f in files:
                        ext = os.path.splitext(f)[1].lower()
                        if ext in supported:
                            full_p = os.path.join(root, f)
                            rel_p = os.path.relpath(full_p, local_path)
                            found_files.append({
                                "select": True,
                                "path": rel_p,
                                "full_path": full_p,
                                "size_kb": os.path.getsize(full_p) / 1024,
                                "type": ext[1:].upper()
                            })
                
                if not found_files:
                    st.warning("No supported files found inside this folder.")
                    st.session_state.scanned_files = None
                else:
                    st.session_state.scanned_files = found_files
                    st.session_state.scanned_path = local_path
                    st.rerun()

    if st.session_state.scanned_files:
        st.success(f"Found **{len(st.session_state.scanned_files)}** matching files in **{st.session_state.scanned_path}**:")
        
        # Display editable checkout dataframe
        scanned_df = pd.DataFrame(st.session_state.scanned_files)
        edited_df = st.data_editor(
            scanned_df,
            column_config={
                "select": st.column_config.CheckboxColumn("Convert?", default=True),
                "path": st.column_config.TextColumn("Relative Path", width="medium"),
                "size_kb": st.column_config.NumberColumn("Size", format="%.1f KB"),
                "type": st.column_config.TextColumn("Format"),
                "full_path": None  # Hide full path
            },
            disabled=["path", "size_kb", "type"],
            use_container_width=True,
            hide_index=True,
            key="local_file_editor"
        )
        
        # Capture selected files
        selected_rows = edited_df[edited_df["select"] == True]
        if not selected_rows.empty:
            source_mode = "local"
            for _, r in selected_rows.iterrows():
                files_to_process.append({
                    "name": r["path"],
                    "full_path": r["full_path"],
                    "is_zip": r["path"].lower().endswith(".zip")
                })
            st.write(f"📂 Selected **{len(files_to_process)}** file(s) from local folder.")

# Run Conversion Pipeline
if files_to_process:
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Start Conversion Process"):
        progress_box = st.empty()
        
        # UI updates callback passed to the parser backend
        def update_ui_cb(filename, file_index, total_files, detail_text):
            progress_box.markdown(
                show_loading_spinner(filename, f"File {file_index} of {total_files} | {detail_text}"),
                unsafe_allow_html=True
            )
            
        zip_data, results, duration = run_conversion_pipeline(files_to_process, source_mode, update_ui_cb)
        progress_box.empty()
        
        # Check if output should be direct single file format
        is_single = (source_mode == "browser" and len(files_to_process) == 1 and not files_to_process[0]["is_zip"])
        st.session_state.is_single_output = is_single
        
        if is_single and results:
            out_name = list(results.keys())[0]
            st.session_state.single_file_name = out_name
            st.session_state.single_file_content = results[out_name]["content"]
        else:
            st.session_state.single_file_name = ""
            st.session_state.single_file_content = ""
            
        st.session_state.converted_zip = zip_data
        st.session_state.converted_results = results
        st.session_state.conversion_time = duration
        st.session_state.conversion_done = True
        st.rerun()

# Conversion Results Dashboard
if st.session_state.conversion_done:
    # 1. Place results anchor at the top of results dashboard
    st.markdown('<div id="results-anchor"></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Conversion Summary")
    
    results_dict = st.session_state.converted_results
    total_converted = len(results_dict)
    successful = sum(1 for item in results_dict.values() if item["status"] == "Success")
    failed = total_converted - successful
    total_size = sum(item["size_kb"] for item in results_dict.values())
    
    # Showcase stats columns with Neo-Brutalist cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_converted}</div>
            <div class="metric-label">Total Files</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="background: #E8F5E9; border-color: #39FF14;">
            <div class="metric-value" style="color: #2E7D32;">{successful}</div>
            <div class="metric-label">Successful</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: #FFEBEE; border-color: #FF007F;">
            <div class="metric-value" style="color: #C62828;">{failed}</div>
            <div class="metric-label">Errors</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_size:.1f} KB</div>
            <div class="metric-label">Markdown Size</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"<div style='text-align: right; color: #57534E; font-size: 0.85rem; margin-top: 10px; font-weight:700;'>Completed in <b>{st.session_state.conversion_time:.2f}s</b></div>", unsafe_allow_html=True)
    
    # File listing details table
    st.markdown("#### Document Status List")
    status_rows = []
    for out_name, val in results_dict.items():
        status_rows.append({
            "Output File": out_name,
            "Original Name": val["name"],
            "Status": "✅ Success" if val["status"] == "Success" else f"❌ {val['status']}",
            "Markdown Size": f"{val['size_kb']:.2f} KB" if val["status"] == "Success" else "N/A"
        })
    st.table(pd.DataFrame(status_rows))
    
    # File download triggers
    st.markdown("#### 📥 Retrieve Converted Output")
    
    if st.session_state.is_single_output:
        st.download_button(
            label="📥 Download Converted Markdown (.MD)",
            data=st.session_state.single_file_content,
            file_name=st.session_state.single_file_name,
            mime="text/markdown"
        )
    else:
        st.download_button(
            label="📥 Download Converted Markdowns (.ZIP)",
            data=st.session_state.converted_zip,
            file_name="converted_markdowns.zip",
            mime="application/zip"
        )

    # 2. Inject iframe JS component to scroll to results and expand sidebar programmatically
    # Safe Guard: Try/Catch blocks prevent script termination if Same-Origin Policy is violated under embedding domains.
    components.html("""
    <script>
        setTimeout(function() {
            try {
                var parentDoc = window.parent.document;
                
                // Expand sidebar if it is collapsed
                var sidebarButton = parentDoc.querySelector('button[data-testid="collapsedSidebar"]');
                if (sidebarButton) {
                    sidebarButton.click();
                }
                
                // Scroll to the results summary element
                var resultsAnchor = parentDoc.getElementById("results-anchor");
                if (resultsAnchor) {
                    resultsAnchor.scrollIntoView({behavior: "smooth", block: "start"});
                }
            } catch (e) {
                console.warn("Same-Origin Policy restricted parent document access from iframe context:", e);
            }
        }, 300);
    </script>
    """, height=0, width=0)