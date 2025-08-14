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
    st.subheader("Upload inputs or use example data")

    # Create two new column containers
    col1, col2 = st.columns(2)

    with col1:
        # Upload input files
        counts_file = st.file_uploader("Counts (TSV with gene_id in first column)", type=["tsv", "txt"])
        samples_file = st.file_uploader("Samples (CSV with columns: sample, condition[, batch])", type=["csv"])

        # Submit button for input data
        if st.button("Submit data"):
            if counts_file and samples_file:
                saved_counts = save_uploaded_file(counts_file, project_root / "inputs")
                st.session_state["counts_path"] = str(saved_counts)
                saved_samples = save_uploaded_file(samples_file, project_root / "inputs")
                st.session_state["samples_path"] = str(saved_samples)
                st.success("Loaded user data.")
            elif counts_file:
                st.write("Missing column data.")
            elif samples_file:
                st.write("Missing counts matrix.")
            else:
                st.write("No data provided.")

        # Button to use provided example data
        if st.button("Use example data"):
            counts_path = Path("data/example/counts.tsv")
            samples_path = Path("data/example/samples.csv")
            st.session_state["counts_path"] = str(counts_path)
            st.session_state["samples_path"] = str(samples_path)
            st.success("Loaded example data.")

    with col2:
        # Saves a preview of the dataframe in the second column
        cp = st.session_state.get("counts_path")
        sp = st.session_state.get("samples_path")
        if cp and sp:
            st.caption(f"Count matrix preview: {cp}")
            st.dataframe(read_table_preview(Path(cp)))
            st.caption(f"Column data preview: {sp}")
            st.dataframe(read_table_preview(Path(sp)))

with tab_params:
    st.write("Hello World!")

with tab_run:
    st.write("Hello World!")

with tab_results:
    st.write("Hello world!")