import time
from query_faiss import query_faiss
from query_neo4j import query_neo4j

def time_query(query, method):
    start_time = time.time()
    if method == "faiss":
        result = query_faiss(query, index, texts)
    elif method == "neo4j":
        result = query_neo4j(query)
    end_time = time.time()
    return end_time - start_time

if __name__ == "__main__":
    query = "Your query here"
    faiss_time = time_query(query, "faiss")
    neo4j_time = time_query(query, "neo4j")

    print(f"FAISS Query Time: {faiss_time} seconds")
    print(f"Neo4j Query Time: {neo4j_time} seconds")
