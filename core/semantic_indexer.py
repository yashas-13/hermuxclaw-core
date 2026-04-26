import os
import json
import math

class SemanticIndexer:
    """
    Semantic Vector Database for Hermuxclaw.
    Embeds code descriptions and AST summaries into high-dimensional space
    to enable intelligent intent-based harvesting and retrieval.
    """
    def __init__(self):
        self.index_file = os.path.expanduser("~/hermuxclaw/memory/semantic_index.json")
        self.index = self._load_index()

    def _load_index(self):
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_index(self):
        with open(self.index_file, "w") as f:
            json.dump(self.index, f, indent=2)

    def embed(self, text, input_type="query"):
        from openai import OpenAI
        try:
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=os.environ.get("NIM_API_KEY", "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")
            )
            # Truncate text to ensure it fits within embedding context limits
            clean_text = text.replace('\n', ' ')[:8000]
            res = client.embeddings.create(
                input=[clean_text],
                model="nvidia/nv-embedqa-e5-v5",
                encoding_format="float",
                extra_body={"input_type": input_type}
            )
            return res.data[0].embedding
        except Exception as e:
            print(f"[!] Embedding Failed: {e}")
            return None

    def add_document(self, doc_id, text, metadata=None):
        vector = self.embed(text, input_type="passage")
        if vector:
            self.index[doc_id] = {
                "vector": vector,
                "metadata": metadata or {},
                "text_snippet": text[:200]
            }
            self._save_index()
            return True
        return False

    def cosine_similarity(self, v1, v2):
        dot_product = sum(a*b for a, b in zip(v1, v2))
        magnitude_v1 = math.sqrt(sum(a*a for a in v1))
        magnitude_v2 = math.sqrt(sum(b*b for b in v2))
        if magnitude_v1 * magnitude_v2 == 0:
            return 0.0
        return dot_product / (magnitude_v1 * magnitude_v2)

    def search(self, query, top_k=3, threshold=0.7):
        query_vector = self.embed(query, input_type="query")
        if not query_vector:
            return []
            
        results = []
        for doc_id, data in self.index.items():
            sim = self.cosine_similarity(query_vector, data["vector"])
            if sim >= threshold:
                results.append({
                    "id": doc_id,
                    "score": sim,
                    "metadata": data["metadata"],
                    "snippet": data["text_snippet"]
                })
                
        # Sort by highest similarity
        return sorted(results, key=lambda x: x["score"], reverse=True)[:top_k]

if __name__ == "__main__":
    idx = SemanticIndexer()
    print("[*] Semantic Index initialized. Current documents:", len(idx.index))
