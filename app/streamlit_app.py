import streamlit as st

# Define the pages
main_page = st.Page("home_page.py", title="Home Page")
page_2 = st.Page("page_2.py", title="DESeq Analysis")

# Set up navigation
pg = st.navigation([main_page, page_2])

# Run the selected page
pg.run()