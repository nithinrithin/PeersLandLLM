from src.config import (
    REPO_URL, REPO_PATH, OUTPUT_PATH,
    LLM_PROVIDER, OPENAI_API_KEY, GOOGLE_API_KEY
)
from src.ingest.clone_repo import clone_repo
from src.ingest.file_loader import collect_code_files
from src.processing.chunker import chunk_code
# from src.llm.analyser import analyze_chunks
from src.llm.analyzer_google import analyze_chunks
from src.utils.json_writer import write_json
from semaintic_chunk_filter import SemanticChunkFilter

# Choose analyzer dynamically
if LLM_PROVIDER == "openai":
    print("Using OpenAI LLM")
    from src.llm.analyzer_openai import analyze_chunks
    def analyze(chunks): return analyze_chunks(chunks, OPENAI_API_KEY)
else:
    print("Using Google LLM")
    from src.llm.analyzer_google import analyze_chunks
    def analyze(chunks): return analyze_chunks(chunks, GOOGLE_API_KEY)


def main():
    clone_repo(REPO_URL, REPO_PATH)
    code_files = collect_code_files(REPO_PATH)
    chunks = chunk_code(code_files)
    filterer = SemanticChunkFilter(backend="huggingface")  # or "openai"
    filtered_chunks = filterer.filter(chunks, query="MavenWrapperDownloader", threshold = 0, top_k=0)
    print(f"Filtered down to {len(filtered_chunks)} chunks:")
    for chunk in filtered_chunks:
        print(f"Path: {chunk.get('path', 'N/A')}, Similarity: {chunk['similarity']:.4f}")
    # results = analyze(chunks)
    # write_json(results, OUTPUT_PATH)

if __name__ == "__main__":
    main()
