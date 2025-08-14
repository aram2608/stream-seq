import streamlit as st

# Define the pages
main_page = st.Page("home_page.py", title="Home Page")
deseq = st.Page("deseq.py", title="DESeq Analysis")
file_wiz = st.Page("file_wiz.py", title="File Formatter")

# Set up navigation
pg = st.navigation([main_page, deseq, file_wiz])

# Run the selected page
pg.run()