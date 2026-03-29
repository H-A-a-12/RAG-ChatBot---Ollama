import streamlit as st
from query_neo4j import query_neo4j

st.title("PDF Chat with Neo4j Vector")

query = st.text_input("Enter your query:")
if query:
    result = query_neo4j(query)
    st.write(result)
