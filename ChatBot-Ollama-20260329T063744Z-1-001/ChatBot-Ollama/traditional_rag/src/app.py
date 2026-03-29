import streamlit as st
from query_faiss import query_faiss

st.title("PDF Chat with Traditional RAG")

query = st.text_input("Enter your query:")
if query:
    result = query_faiss(query, index, texts)
    st.write(result)
