import os
import faiss  # type: ignore[import-untyped]
import numpy as np 
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()
VECTOR_DIM = 1536 #openAI embedding dimension 
index = faiss.IndexFlatL2(VECTOR_DIM)

documents = []

def chunk_text(text, chunk_size=500):
    chunk = []
    for i in range(0, len(text), chunk_size):
        chunk.append(text[i:i+chunk_size])
    return chunk

def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding


def load_knowledge():
    global documents

    knowledge_dir = "knowledge"

    for filename in os.listdir(knowledge_dir):
        with open(os.path.join(knowledge_dir, filename), "r", encoding="utf-8") as f:
            content = f.read()

            chunks = chunk_text(content)

            for chunk in chunks:
                documents.append(chunk)
                vector = embed_text(content)
                index.add(np.array([vector]).astype("float32"))

    
def search_similar(query, top_k=2):
    query_vector = embed_text(query)
    D, I = index.search(
        np.array([query_vector]).astype("float32"),
        top_k,
    )

    results = [documents[i] for i in I[0]]
    return results