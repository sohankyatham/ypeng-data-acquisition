import streamlit as st
import pandas as pd

st.title("Analyze Data Page")
st.write("Hello World! This is the Analyze Data page.")

st.write("Use the tools below to upload your data, preview it, and perform basic analysis.")

# Upload
st.markdown("### 🔼 Upload Data File")
uploaded_file = st.file_uploader("Upload CSV, Excel, or text data files", type=['csv', 'xlsx', 'txt'])
