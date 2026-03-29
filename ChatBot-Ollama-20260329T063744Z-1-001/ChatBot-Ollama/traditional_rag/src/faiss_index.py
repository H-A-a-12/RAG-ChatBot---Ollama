import faiss
import numpy as np

def build_faiss_index(embeddings):
    index = faiss.IndexFlatL2(embeddings.shape)
    index.add(np.array(embeddings))
    return index

if __name__ == "__main__":
    embeddings = np.load('embeddings.npy')
    index = build_faiss_index(embeddings)
    faiss.write_index(index, 'faiss_index.index')
