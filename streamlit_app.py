from click import File
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Guidance Finder",
    layout="wide"
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
    ">
        Guidance Finder
    </h1>
  </div>
  """, unsafe_allow_html=True
)

def reset_search():
      st.session_state["search"] = ""
      st.session_state["system"] = "All"
      st.session_state["category"] = "All"
st.button(
    "Reset Search", on_click=reset_search)

search = st.text_input("Search by title, summary or keyword?",
    key="search")
search= search.strip()

df = pd.read_csv("Guidance Database Prototype CSV.csv")
guidance_folder = "Guidance Files"

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

else:
     st.success(f"Found {len(results)} guidance document(s) matching your search criteria.")

     for _, row in results.iterrows():
         title = row["Title"]
         summary = row["Summary"]
         system = row["System"]
         category = row["Category"]
         filename = row["File"]

         file_path = os.path.join(guidance_folder, filename)
         if os.path.exists(file_path):
             with open(file_path, "rb") as f:
                 file_bytes = f.read()
             st.markdown(f"### {title}")
             st.markdown(f"**System:** {system} | **Category:** {category}")
             st.markdown(f"**Summary:** {summary}")
             st.download_button(
                 label="Download Guidance Document",
                 data=file_bytes,
                 file_name=filename,
                 mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
             )
             st.markdown("---")
         else:
             st.warning(f"File '{filename}' not found in the guidance folder.")