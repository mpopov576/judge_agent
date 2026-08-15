import chromadb
import uuid

# Persistent local vector DB, so data survives between script runs
client = chromadb.PersistentClient(path="./precedent_db")
collection = client.get_or_create_collection("precedents")

# Looks for similar cases in a distance threshold
def search_precedent(query: str):
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    matched_cases = results["documents"][0]
    distances = results["distances"][0]

    relevant_cases = [
        doc for doc, dist in zip(matched_cases, distances)
        if dist < 1.0
    ]

    if not relevant_cases:
        return {"results": ["No relevant precedent found in the database"]}

    return {"results": relevant_cases }

# Stores the decision in the vector DB
def store_case(case_summary: str):
    case_id = str(uuid.uuid4())

    collection.add(
        documents=[case_summary],
        ids=[case_id]
    )