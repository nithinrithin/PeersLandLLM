import hashlib
from typing import List, Dict, Optional

from sklearn.metrics.pairwise import cosine_similarity

# Optional: HuggingFace
from sentence_transformers import SentenceTransformer

# Optional: LangChain
from langchain.embeddings import OpenAIEmbeddings


class SemanticChunkFilter:
    def __init__(self, backend="openai", model_name="all-MiniLM-L6-v2"):
        self.backend = backend
        self.cache = {}
        SentenceTransformer(model_name, device="cpu")
        SentenceTransformer(model_name, cache_folder="models/")

        if backend == "openai":
            self.embedder = OpenAIEmbeddings()
        elif backend == "huggingface":
            self.embedder = SentenceTransformer(model_name)
        else:
            raise ValueError("Unsupported backend. Use 'openai' or 'huggingface'.")

    def _hash(self, text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()

    def _embed_texts(self, texts: List[str]) -> List:
        vectors = []
        for text in texts:
            key = self._hash(text)
            if key in self.cache:
                vectors.append(self.cache[key])
            else:
                if self.backend == "openai":
                    vector = self.embedder.embed_query(text)
                else:
                    vector = self.embedder.encode(text)
                self.cache[key] = vector
                # print(vector)
                vectors.append(vector)
        return vectors

    def filter(self, chunks: List[Dict], query: str, threshold: float = 0.75, top_k: Optional[int] = None) -> List[Dict]:
        chunk_texts = [chunk["page_content"] for chunk in chunks]
        chunk_vectors = self._embed_texts(chunk_texts)

        query_vector = self._embed_texts([query])[0]
        scores = cosine_similarity([query_vector], chunk_vectors)[0]

        enriched_chunks = [
            {**chunk, "similarity": score}
            for chunk, score in zip(chunks, scores)
        ]

        if top_k:
            print(f"Selecting top {top_k} chunks based on similarity.")
            return sorted(enriched_chunks, key=lambda x: x["similarity"], reverse=True)[:top_k]
        else:
            print(f"Filtering chunks with similarity >= {threshold}.")
            for chunk in enriched_chunks:
                print(f"Path: {chunk.get('path', 'N/A')}, Similarity: {chunk['similarity']:.4f}")
            return [chunk for chunk in enriched_chunks if chunk["similarity"] >= threshold]
