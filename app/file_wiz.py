from pathlib import Path
from utils import save_uploaded_file, ensure_project_dirs, read_table_preview, which, read_table_wiz

import streamlit as st
import pandas as pd

st.set_page_config(page_title="File Formatter", layout="wide")
st.title("File Formatter")

# Set up out project root and associated directories for I/O
project_root = Path(st.text_input("Project directory", value="viewer"))
if st.button("Load directory with files you wish to view"):
    ensure_project_dirs(project_root)
    st.success("Directory saved with necessary sub directories.")

file_viewer, formatter = st.tabs(["File Viewer", "Formatter"])

with file_viewer:
    st.subheader("Upload inputs or use example data")

    # Upload input files
    file = st.file_uploader(
        "File you wish to view", type=["tsv", "txt", "csv"]
    )

    if st.button("Submit data"):
        if file:
            saved_file = save_uploaded_file(file, project_root / "inputs")
            st.session_state["file_path"] = str(saved_file)
            st.success("Loaded user data.")
        else:
            st.write("No data provided.")

    # Use example data
    if st.button("Use example"):
        file = Path("data/example/counts.tsv")
        st.session_state["file_path"] = str(file)
        st.success("Loaded example data.")

    if file:
        f = st.session_state.get("file_path")
        if f:
            st.caption(f"File: {f}")
            st.dataframe(read_table_preview(Path(f)))

with formatter:
    # Save file to session state to make it persistent across changes
    if file:
        st.session_state.file_path = file

    # Check to ensure the file is currently in session state
    if "file_path" in st.session_state:
        f = st.session_state.file_path
        n = st.slider("Select number of columns", 20, 100, 20)
        df = read_table_wiz(Path(f), n)
        st.dataframe(df)
    else:
        st.subheader("Upload file to reformat")