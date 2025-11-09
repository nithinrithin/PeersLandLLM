import time
import asyncio
from src.utils.logger import setup_logger
logger = setup_logger()

from src.config import (
    REPO_URL, REPO_PATH, OUTPUT_PATH,
    LLM_PROVIDER, OPENAI_API_KEY, GOOGLE_API_KEY, LLM_MODEL
)

from src.ingest.clone_repo import clone_repo
from src.ingest.file_loader import collect_code_files_async
from src.processing.chunker import chunk_code_async
# from src.processing.chunker import chunk_code_tree_based as chunk_code_async
from src.utils.json_writer import stream_json_output_async


if LLM_PROVIDER == "openai":
    from src.llm.analyzer_openai import analyze_chunks_async
    def analyze(chunks): return analyze_chunks_async(chunks, OPENAI_API_KEY, LLM_MODEL)
else:
    from src.llm.analyzer_google import analyze_chunks_async
    def analyze(chunks): return analyze_chunks_async(chunks, GOOGLE_API_KEY, LLM_MODEL)

async def main():
    start_time = time.time()
    logger.info("Starting asynchronous code analysis...")

    clone_repo(REPO_URL, REPO_PATH)
    files = await collect_code_files_async(REPO_PATH)
    chunks = await chunk_code_async(files)
    results = await analyze(chunks)
    await stream_json_output_async(results, OUTPUT_PATH)
    
    logger.info("Asynchronous code analysis completed.")
    logger.info("Results saved to %s", OUTPUT_PATH)
    logger.info("Total time taken: %s seconds", time.time() - start_time)

if __name__ == "__main__":
    asyncio.run(main())
