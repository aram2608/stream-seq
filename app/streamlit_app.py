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
if st.button("Load project directory"):
    ensure_project_dirs(project_root)
    st.success("Directory saved with necessary sub directories.")

# Create tabs for I/O operations
tab_input, tab_params, tab_run, tab_results = st.tabs(
    ["Inputs", "Parameters", "Run", "Results"]
)

#########
# I/O Tab
#########
with tab_input:
    st.subheader("Upload inputs or use example data")

    # Create two new column containers
    col1, col2 = st.columns(2)

    with col1:
        # Upload input files
        counts_file = st.file_uploader(
            "Counts (TSV with gene_id in first column)", type=["tsv", "txt"]
        )
        samples_file = st.file_uploader(
            "Samples (CSV with columns: sample, condition[, batch])", type=["csv"]
        )

        # Submit button for input data
        if st.button("Submit data"):
            if counts_file and samples_file:
                saved_counts = save_uploaded_file(counts_file, project_root / "inputs")
                st.session_state["counts_path"] = str(saved_counts)
                saved_samples = save_uploaded_file(
                    samples_file, project_root / "inputs"
                )
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

#########
# Parameter tab
#########
with tab_params:
    st.subheader("Analysis parameters")

    # Parameters to be used in DESeq
    counts_path = st.session_state.get("counts_path", "")
    samples_path = st.session_state.get("samples_path", "")
    design = st.text_input("Design formula (R syntax)", value="~ condition")
    outdir = st.text_input("Output directory", value=str(project_root / "results"))

    # TODO: Add support for these functions later
    st.markdown(":orange-badge[⚠️ Not currently supported]")
    species = st.text_input(
        "Species annotation package", value="org.Hs.eg.db", disabled=True
    )
    use_tximport = st.checkbox(
        "Use tximport (Kallisto/Salmon)", value=False, disabled=True
    )
    tximport_dir = st.text_input(
        "Tximport directory (folder with quant files)", value="", disabled=True
    )

    # Saves the analysis parameters for the session
    st.session_state["config"] = AnalysisConfig(
        counts=counts_path,
        samples=samples_path,
        design=design,
        outdir=outdir,
        species=species or None,
        use_tximport=use_tximport,
        tximport_dir=tximport_dir or None,
    )

    # Exports parameters to JSON config file
    if st.button("Save config"):
        cfg = st.session_state["config"]
        path = project_root / "config" / "analysis.json"
        cfg.write_json(path)
        st.success(f"Saved config → {path}")

#########
# Tab to run analysis
#########
with tab_run:
    st.subheader("Run analysis")
    col1, col2 = st.columns(2)

    with col1:
        # Load our R script
        rscript = Path("r_engine/run_deseq.R")
        st.text(f"Rscript path: {rscript}")
        if which("Rscript") is None:
            st.error("Rscript not found on PATH. Activate the conda env first.")
        else:
            # Button to run the R script
            if st.button("Run R engine"):
                # Retrieve a key from the session state
                cfg = st.session_state.get("config")
                if not cfg:
                    st.error("Please configure parameters first.")
                else:
                    cfg_path = project_root / "config" / "analysis.json"
                    cfg.write_json(cfg_path)
                    with st.status("Running R engine…", expanded=True) as status:
                        result = run_r_engine(rscript, cfg_path, workdir=Path("."))

                        # Write out the outputs and errors produced
                        st.write("**STDOUT**")
                        st.code(result.stdout)
                        st.write("**STDERR**")
                        st.code(result.stderr)

                        # Test for succesful execution
                        if result.returncode == 0:
                            status.update(label="Success", state="complete")
                            st.success("Analysis completed.")
                        else:
                            status.update(label="Failed", state="error")
                            st.error(
                                f"R engine failed with exit code {result.returncode}"
                            )
#########
# Results tab
#########
with tab_results:
    st.write("Hello world!")
