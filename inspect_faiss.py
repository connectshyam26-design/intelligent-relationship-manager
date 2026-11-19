from app.rag import index, documents, metadata

print("Number of vectors:", index.ntotal)
print("Vector dimension:", index.d)

print("\nDocuments:")
for i, doc in enumerate(documents):
    print(f"\nID: {i}")
    print("Source:", metadata[i]["source"])
    print("Content:")
    print(doc)