import streamlit as st
from pathlib import Path
import pandas as pd
from config import AnalysisConfig
from orchestrator import run_r_engine
from utils import save_uploaded_file, ensure_project_dirs, read_table_preview, which

# Set the page title
st.set_page_config(page_title="stream-seq (Python + R/DESeq2)", layout="wide")
st.title("stream-seq — Python UI + R/DESeq2 Engine")

# Set up out project root and associated directories for I/O
project_root = Path(st.text_input("Project directory", value="project"))
ensure_project_dirs(project_root)

# Create tabs for I/O operations
tab_input, tab_params, tab_run, tab_results = st.tabs(["Inputs", "Parameters", "Run", "Results"])

with tab_input:
    st.write("Hellow World!")

with tab_params:
    st.write("Hello World!")

with tab_run:
    st.write("Hello World!")

with tab_results:
    st.write("Hello world!")