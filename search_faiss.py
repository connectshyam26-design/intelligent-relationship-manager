from app.rag import embedding_model, index, documents, metadata

query = "Which account is suitable for a customer earning 9 lakh?"

query_vector = embedding_model.encode(
    [query],
    normalize_embeddings=True
)

scores, indices = index.search(query_vector, 3)

print("Query:", query)

for rank, (score, idx) in enumerate(
    zip(scores[0], indices[0]),
    start=1
):
    print(f"\nRank: {rank}")
    print("FAISS ID:", idx)
    print("Similarity score:", float(score))
    print("Source:", metadata[idx]["source"])
    print("Content:")
    print(documents[idx])