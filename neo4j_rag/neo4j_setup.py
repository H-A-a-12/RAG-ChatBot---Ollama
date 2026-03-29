from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def create_nodes(tx, texts, embeddings):
    for i, text in enumerate(texts):
        tx.run("CREATE (n:Document {id: $id, text: $text, embedding: $embedding})",
               id=i, text=text, embedding=embeddings[i].tolist())

if __name__ == "__main__":
    texts = load_pdf('../data/your_pdf_file.pdf')
    embeddings = create_embeddings(texts)
    with driver.session() as session:
        session.write_transaction(create_nodes, texts, embeddings)
