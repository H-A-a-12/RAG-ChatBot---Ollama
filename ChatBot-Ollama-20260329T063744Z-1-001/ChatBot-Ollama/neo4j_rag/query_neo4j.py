from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def query_neo4j(query):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query]).tolist()
    with driver.session() as session:
        result = session.run("MATCH (n:Document) "
                             "RETURN n.text AS text, "
                             "gds.similarity.cosine(n.embedding, $embedding) AS similarity "
                             "ORDER BY similarity DESC LIMIT 1",
                             embedding=query_embedding)
        return result.single()["text"]

if __name__ == "__main__":
    query = "Your query here"
    result = query_neo4j(query)
    print(result)
