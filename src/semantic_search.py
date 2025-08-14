import json
import os
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize the semantic search model
print("Loading sentence transformer model...")
model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight but effective model
print("Model loaded successfully!")


def get_db_connection():
    """Get database connection."""
    db_path = os.path.join("/Users/dan.popa/work/mcp-hackathon/src", "commits.db")
    return sqlite3.connect(db_path)


def semantic_search_commits(query: str, search_type: str = "both", top_k: int = 10):
    """
    Perform semantic search on commits using embeddings.

    Args:
        query: Search query string
        search_type: "diffs", "reason", or "both" to specify which embeddings to search
        top_k: Number of top results to return

    Returns:
        List of matching commits with similarity scores
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Encode the query
    query_embedding = model.encode(query)

    results = []

    if search_type in ["diffs", "both"]:
        # Search in diffs embeddings
        cursor.execute("""
            SELECT rowid, repo, sha, title, diffs, reason, diffs_embedding
            FROM commits 
            WHERE diffs_embedding IS NOT NULL
        """)

        diffs_records = cursor.fetchall()
        for record in diffs_records:
            rowid, repo, sha, title, diffs, reason, diffs_embedding_json = record
            if diffs_embedding_json:
                diffs_embedding = np.array(json.loads(diffs_embedding_json))
                similarity = np.dot(query_embedding, diffs_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(diffs_embedding)
                )
                results.append(
                    {
                        "rowid": rowid,
                        "repo": repo,
                        "sha": sha,
                        "title": title,
                        "diffs": diffs[:500] + "..." if len(diffs) > 500 else diffs,
                        "reason": reason,
                        "similarity": float(similarity),
                        "search_field": "diffs",
                    }
                )

    if search_type in ["reason", "both"]:
        # Search in reason embeddings
        cursor.execute("""
            SELECT rowid, repo, sha, title, diffs, reason, reason_embedding
            FROM commits 
            WHERE reason_embedding IS NOT NULL
        """)

        reason_records = cursor.fetchall()
        for record in reason_records:
            rowid, repo, sha, title, diffs, reason, reason_embedding_json = record
            if reason_embedding_json:
                reason_embedding = np.array(json.loads(reason_embedding_json))
                similarity = np.dot(query_embedding, reason_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(reason_embedding)
                )
                results.append(
                    {
                        "rowid": rowid,
                        "repo": repo,
                        "sha": sha,
                        "title": title,
                        "diffs": diffs[:500] + "..." if len(diffs) > 500 else diffs,
                        "reason": reason,
                        "similarity": float(similarity),
                        "search_field": "reason",
                    }
                )

    conn.close()

    # Sort by similarity and return top_k
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]
