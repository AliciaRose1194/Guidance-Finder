from numpy import insert
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Guidance Finder",
    layout="wide",
    page_icon="getsitelogo.png",
)
st.markdown("""
  <div style="
    background-color:#1A6235;
    padding: 20px;
    border-radius: 8px;
    margin-bottom:20px;
">
    <h1 style="
        color:white;
        margin: 0;
        text-align: left;
        padding-left: 300px;
    ">
        Guidance Finder
    </h1>
    <h5 style="
    color:white;
    margin:0;
    text-align: left;
    padding-left: 300px;">
        <p>Search Internal Guidance Documents</p>
    </h5>
  </div>
  """, unsafe_allow_html=True
)

def reset_search():
      st.session_state["search"] = ""
      st.session_state["system"] = "All"
      st.session_state["category"] = "All"
st.button(
    "Reset Search", on_click=reset_search)

df = pd.read_csv("Guidance Database Prototype CSV.csv")
guidance_folder = "Guidance Files"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Documents", len(df))
with col2:
    st.metric("Systems", df["System"].nunique())
with col3:
    st.metric("Categories", df["Category"].nunique())
search = st.text_input("Search by title, summary or keyword?",
    key="search")
search= search.strip()
system = st.selectbox(
    "Filter by system",
    ["All"] +
sorted (df["System"].dropna().unique().tolist()),
    key="system"
)
category = st.selectbox (
    "Filter by category",
    ["All"] +
sorted (df["Category"].dropna().unique().tolist()),
    key="category"
)
has_filters = (
    search.strip() != "" or
    system != "All" or
    category != "All"
)
if not has_filters:
     st.info("Enter a search term or choose a filter to view guidance.")
else:
    if search:
         results = df[
    (df["Title"].str.contains(search, case=False, na=False)) |
    (df["Summary"].str.contains(search, case=False, na=False)) |
    (df["Keywords"].str.contains(search, case=False, na=False))
    ]
    else:
        results = df
    if system != "All":
        results = results[results["System"] == system]

    if category != "All":
        results = results[results["Category"] == category]

    if len(results) == 0:
        st.error(
        "No guidance documents found matching your search criteria.\n\n" "Please try a different search term or select 'Reset Search' to clear.")
    else:
        st.success(f"Found {len(results)} guidance document(s) matching your search criteria.")
        for _, row in results.iterrows():
            title = row["Title"]
            summary = row["Summary"]
            system_val = row["System"]
            category_val = row["Category"]
            filename = str(row.get("File", "")).strip()
            file_path = os.path.join(guidance_folder, filename)
            with st.expander(title):
                if not filename:
                    st.warning("No file specified for this guidance.")
                elif os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()
                    st.markdown(f"**System:** {system_val} | **Category:** {category_val}")
                    st.markdown(f"**Summary:** {summary}")
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()
                    if ext == ".docx":
                        mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    elif ext == ".pdf":
                        mime = "application/pdf"
                    else:
                        mime = "application/octet-stream"
                    st.download_button(
                        label=f"Download {title}",
                        data=file_bytes,
                        file_name=filename,
                        mime=mime
                    )
                else:
                    st.warning(f"File '{filename}' not found in the guidance folder.")
st.markdown("___")
st.caption("Guidance Finder Prototype 2026 - Alicia R Fell - LCC")