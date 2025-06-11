Rewritten version of the FAISS-based semantic search pipeline using **6 different vector databases**:

---

### ✅ Shared setup

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# 1. Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Prepare documents
documents = [
    "Cats are independent pets.",
    "Dogs are loyal and friendly animals.",
    "Birds can fly and live in trees.",
    "Fish live in water and need aquariums.",
    "Tigers are wild animals found in forests."
]

# 3. Embed documents
doc_embeddings = model.encode(documents)
query = "Which animals make good pets?"
query_embedding = model.encode([query])[0]
```

---

## 1️⃣ **Chroma**

```python
import chromadb
from chromadb.utils import embedding_functions

# 4. Create Chroma client
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="animals")

# 5. Add documents
collection.add(
    documents=documents,
    embeddings=[vec.tolist() for vec in doc_embeddings],
    ids=[str(i) for i in range(len(documents))]
)

# 6. Query
results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=3
)

# 7. Print
for match in results["documents"][0]:
    print(match)
```

---

## 2️⃣ **Pinecone**

```python
import pinecone

pinecone.init(api_key="YOUR_API_KEY", environment="YOUR_ENV")
dimension = doc_embeddings.shape[1]
index_name = "animals"

if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, dimension=dimension, metric="cosine")

index = pinecone.Index(index_name)
index.upsert([
    (str(i), vec.tolist(), {"text": documents[i]})
    for i, vec in enumerate(doc_embeddings)
])

results = index.query(
    vector=query_embedding.tolist(),
    top_k=3,
    include_metadata=True
)

for match in results["matches"]:
    print(match["metadata"]["text"])
```

---

## 3️⃣ **Weaviate**

```python
import weaviate
from weaviate.embedded import EmbeddedOptions

client = weaviate.Client(embedded_options=EmbeddedOptions())

schema = {
    "classes": [{
        "class": "Animal",
        "vectorizer": "none",
        "properties": [{"name": "text", "dataType": ["text"]}]
    }]
}
client.schema.create(schema)

for i, vec in enumerate(doc_embeddings):
    client.data_object.create(
        {"text": documents[i]}, class_name="Animal", vector=vec.tolist()
    )

results = client.query.get("Animal", ["text"]).with_near_vector({
    "vector": query_embedding.tolist()
}).with_limit(3).do()

for obj in results['data']['Get']['Animal']:
    print(obj["text"])
```

---

## 4️⃣ **Qdrant**

```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(":memory:")
dimension = doc_embeddings.shape[1]

client.recreate_collection(
    collection_name="animals",
    vectors_config=VectorParams(size=dimension, distance=Distance.COSINE)
)

client.upsert(
    collection_name="animals",
    points=[
        PointStruct(id=i, vector=vec.tolist(), payload={"text": documents[i]})
        for i, vec in enumerate(doc_embeddings)
    ]
)

results = client.search(
    collection_name="animals",
    query_vector=query_embedding.tolist(),
    limit=3
)

for res in results:
    print(res.payload["text"])
```

---

## 5️⃣ **Milvus**

```python
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
import uuid

connections.connect("default", host="localhost", port="19530")

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=doc_embeddings.shape[1])
]

schema = CollectionSchema(fields, description="Animal vector DB")
collection = Collection("animals", schema)

data = [
    [i for i in range(len(documents))],
    documents,
    [vec.tolist() for vec in doc_embeddings]
]
collection.insert(data)
collection.load()

search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = collection.search(
    data=[query_embedding.tolist()],
    anns_field="embedding",
    param=search_params,
    limit=3,
    output_fields=["text"]
)

for hit in results[0]:
    print(hit.entity.get("text"))
```

---

## 6️⃣ **PGVector (PostgreSQL)**

```python
import psycopg2
import numpy as np

conn = psycopg2.connect("dbname=yourdb user=youruser password=yourpass")
cur = conn.cursor()

# Assumes pgvector is installed and table is created:
# CREATE EXTENSION vector;
# CREATE TABLE animals (id serial PRIMARY KEY, text TEXT, embedding vector(384));

for i, vec in enumerate(doc_embeddings):
    cur.execute(
        "INSERT INTO animals (text, embedding) VALUES (%s, %s)",
        (documents[i], list(vec))
    )
conn.commit()

cur.execute(
    "SELECT text FROM animals ORDER BY embedding <-> %s LIMIT 3;",
    (list(query_embedding),)
)

for row in cur.fetchall():
    print(row[0])
```

---

## ✅ Summary

| Vector DB | Local? | Fully Managed? | Good for RAG?   | Language   |
| --------- | ------ | -------------- | --------------- | ---------- |
| Chroma    | ✅      | ❌              | 🟡 Small-scale  | Python     |
| Pinecone  | ❌      | ✅              | ✅ Scalable      | Python     |
| Weaviate  | ✅/☁️   | ✅              | ✅               | Python     |
| Qdrant    | ✅/☁️   | ✅              | ✅               | Python     |
| Milvus    | ✅      | ☁️ (Zilliz)    | ✅ Large-scale   | Python     |
| PGVector  | ✅      | ❌              | 🟡 Custom setup | SQL/Python |

