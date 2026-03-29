import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer

def load_pdf(file_path):
    doc = fitz.open(file_path)
    texts = [page.get_text() for page in doc]
    return texts

def create_embeddings(texts):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings

if __name__ == "__main__":
    texts = load_pdf('../data/your_pdf_file.pdf')
    embeddings = create_embeddings(texts)
    # Save embeddings for later use
