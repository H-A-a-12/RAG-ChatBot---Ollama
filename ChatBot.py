import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from neo4j import GraphDatabase
import streamlit as st
import time

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load and process the PDF
def load_pdf(file_path):
    doc = fitz.open(file_path)
    texts = []
    for page in doc:
        texts.append(page.get_text())
    return texts

# Create embeddings
def create_embeddings(texts):
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings

# Build FAISS index
def build_faiss_index(embeddings):
    index = faiss.IndexFlatL2(embeddings.shape)
    index.add(np.array(embeddings))
    return index

# Query FAISS
def query_faiss(query, index, texts):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)
    return texts[I]

# Neo4j setup
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# Create nodes and relationships in Neo4j
def create_nodes(tx, texts, embeddings):
    for i, text in enumerate(texts):
        tx.run("CREATE (n:Document {id: $id, text: $text, embedding: $embedding})",
               id=i, text=text, embedding=embeddings[i].tolist())

# Query Neo4j
def query_neo4j(query):
    query_embedding = model.encode([query]).tolist()
    with driver.session() as session:
        result = session.run("MATCH (n:Document) "
                             "RETURN n.text AS text, "
                             "gds.similarity.cosine(n.embedding, $embedding) AS similarity "
                             "ORDER BY similarity DESC LIMIT 1",
                             embedding=query_embedding)
        return result.single()["text"]

# Time comparison
def time_query(query, method):
    start_time = time.time()
    if method == "faiss":
        result = query_faiss(query, index, texts)
    elif method == "neo4j":
        result = query_neo4j(query)
    end_time = time.time()
    return end_time - start_time

# Load PDF and create embeddings
texts = load_pdf('your_pdf_file.pdf')
embeddings = create_embeddings(texts)

# Build FAISS index
index = build_faiss_index(embeddings)

# Create nodes in Neo4j
with driver.session() as session:
    session.write_transaction(create_nodes, texts, embeddings)

# Streamlit UI
st.title("PDF Chat with RAG Approaches")

query = st.text_input("Enter your query:")
if query:
    faiss_result = query_faiss(query, index, texts)
    neo4j_result = query_neo4j(query)
    faiss_time = time_query(query, "faiss")
    neo4j_time = time_query(query, "neo4j")

    st.write("**FAISS Result:**")
    st.write(faiss_result)
    st.write(f"**Query Time:** {faiss_time} seconds")

    st.write("**Neo4j Result:**")
    st.write(neo4j_result)
    st.write(f"**Query Time:** {neo4j_time} seconds")
