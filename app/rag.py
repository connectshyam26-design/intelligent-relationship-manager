from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer


POLICY_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "policies"
)

MODEL_NAME = "all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(MODEL_NAME)

documents = []
metadata = []


def load_policies():
    global documents, metadata

    documents = []
    metadata = []

    for file_path in POLICY_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append(text)

        metadata.append(
            {
                "source": file_path.name
            }
        )


def build_index():
    load_policies()

    embeddings = embedding_model.encode(
        documents,
        normalize_embeddings=True
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


index = build_index()


def search_product_policy(query: str, top_k: int = 2) -> dict:
    """
    Search bank product policy documents.

    Use this tool when the user asks about product eligibility,
    product features, or product policy.

    Args:
        query: Natural language product or policy question.
        top_k: Number of matching policy documents to retrieve.

    Returns:
        Relevant policy documents and their source filenames.
    """

    query_embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True
    )

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        results.append(
            {
                "score": float(score),
                "source": metadata[idx]["source"],
                "content": documents[idx]
            }
        )

    return {
        "status": "success",
        "results": results
    }