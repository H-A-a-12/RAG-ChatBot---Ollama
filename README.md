# 🤖 PDF ChatBot with RAG (FAISS + Neo4j)

A Streamlit-powered chatbot that lets you query PDF documents using two Retrieval-Augmented Generation (RAG) approaches — **FAISS** (vector similarity search) and **Neo4j** (graph-based similarity search) — with real-time query time comparison.

---

## 🧠 How It Works

1. A PDF is loaded and split into page-level text chunks.
2. Each chunk is embedded using a `SentenceTransformer` model (`all-MiniLM-L6-v2`).
3. Embeddings are stored in both:
   - A **FAISS** flat L2 index (in-memory vector store)
   - A **Neo4j** graph database (as `Document` nodes with embedding properties)
4. On user query, both backends retrieve the most relevant chunk and display results side-by-side with query time.

---

## 🗂️ Project Structure

```
├── ChatBot.py          # Main application
├── requirement.txt     # Python dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Prerequisites

- Python 3.8+
- A running [Neo4j](https://neo4j.com/download/) instance (local or cloud)
- Neo4j Graph Data Science (GDS) plugin installed (for `gds.similarity.cosine`)

---

## 🚀 Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/pdf-chatbot-rag.git
cd pdf-chatbot-rag
```

**2. Install dependencies**

```bash
pip install sentence-transformers faiss-cpu transformers streamlit pymupdf neo4j
```

**3. Configure Neo4j connection**

In `ChatBot.py`, update the connection credentials:

```python
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "YOUR_PASSWORD"))
```

**4. Add your PDF**

Place your target PDF in the project root and update this line in `ChatBot.py`:

```python
texts = load_pdf('your_pdf_file.pdf')
```

---

## ▶️ Running the App

```bash
streamlit run ChatBot.py
```

Then open your browser at `http://localhost:8501`.

---

## 🖥️ Usage

1. Launch the app with the command above.
2. Type a question in the text input (e.g., *"What is the conclusion of chapter 3?"*).
3. The app returns the most relevant PDF passage from both **FAISS** and **Neo4j**, along with each method's query time in seconds.

---

## 🧰 Tech Stack

| Component | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io/) |
| PDF Parsing | [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) |
| Embeddings | [SentenceTransformers](https://www.sbert.net/) — `all-MiniLM-L6-v2` |
| Vector Search | [FAISS](https://faiss.ai/) |
| Graph Database | [Neo4j](https://neo4j.com/) + GDS Plugin |

---

## ⚠️ Known Issues & Limitations

- **FAISS index shape bug** — `build_faiss_index` passes `embeddings.shape` instead of `embeddings.shape[1]` as the dimension argument. This will raise a `TypeError` at runtime. Fix:
  ```python
  index = faiss.IndexFlatL2(embeddings.shape[1])  # ✅
  ```

- **FAISS query indexing** — `query_faiss` returns `texts[I]` where `I` is a 2D numpy array. Should be `texts[I[0][0]]` to return a string.

- **Embedding tensor type** — `create_embeddings` uses `convert_to_tensor=True`, but FAISS requires a numpy array. Either remove this flag or call `.numpy()` before passing to FAISS.

- **Neo4j GDS required** — The `gds.similarity.cosine` procedure requires the [GDS plugin](https://neo4j.com/docs/graph-data-science/current/installation/). Without it, Neo4j queries will fail.

- **No persistent FAISS index** — The FAISS index is rebuilt on every app launch. For large PDFs, consider saving/loading with `faiss.write_index` / `faiss.read_index`.

- **Hardcoded PDF path** — The PDF path is hardcoded. Consider adding a Streamlit file uploader for a better UX.

---

## 🔮 Future Improvements

- [ ] Add Streamlit file uploader for dynamic PDF loading
- [ ] Persist FAISS index to disk
- [ ] Support multi-page chunking strategies (e.g., sliding window)
- [ ] Add chat history / conversation memory
- [ ] Deploy to Streamlit Cloud or Docker

---

## 📄 License

This project is open-source. Feel free to fork and extend it.