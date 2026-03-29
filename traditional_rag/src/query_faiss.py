import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def query_faiss(query, index, texts):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)
    return texts[I]

if __name__ == "__main__":
    index = faiss.read_index('faiss_index.index')
    texts = load_pdf('../data/your_pdf_file.pdf')
    query = "Your query here"
    result = query_faiss(query, index, texts)
    print(result)
