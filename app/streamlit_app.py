import streamlit as st

# Define the pages
main_page = st.Page("home_page.py", title="Home Page")
deseq = st.Page("page_2.py", title="DESeq Analysis")
file_wiz = st.Page("page_3.py", title="File Formatter")

# Set up navigation
pg = st.navigation([main_page, deseq, file_wiz])

# Run the selected page
pg.run()