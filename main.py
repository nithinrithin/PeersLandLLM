import time
import asyncio
import aiofiles
from asyncio import Queue
from src.utils.logger import setup_logger
logger = setup_logger()
import argparse

from src.config import (
    REPO_URL, REPO_PATH, OUTPUT_PATH,
    LLM_PROVIDER, OPENAI_API_KEY, GOOGLE_API_KEY, LLM_MODEL
)

from src.ingest.clone_repo import clone_repo
from src.ingest.file_loader import collect_files_async
from src.processing.chunker import chunk_code_async
# from src.processing.chunker import chunk_code_tree_based as chunk_code_async
from src.utils.json_writer import stream_jsonline_output_async


if LLM_PROVIDER == "openai":
    from src.llm.analyzer_openai import analyze_chunks_async
    def analyze(chunks): return analyze_chunks_async(chunks, OPENAI_API_KEY, LLM_MODEL)
else:
    from src.llm.analyzer_google import analyze_chunks_async
    def analyze(chunks): return analyze_chunks_async(chunks, GOOGLE_API_KEY, LLM_MODEL)

# --- Producer: read files asynchronously and enqueue (path, content) ---
async def producer(file_paths, queue, num_consumers):
    for path in file_paths:
        async with aiofiles.open(path, "r") as f:
            content = await f.read()
        await queue.put((path, content))
    # Signal consumers to stop
    for _ in range(num_consumers):
        await queue.put(None)


# --- Consumer: chunk + analyze per file, stream immediately ---
async def consumer(queue, output_path):
    while True:
        item = await queue.get()
        if item is None:
            break
        path, content = item

        # Chunk this single file
        file_docs = [{"path": path, "content": content}]
        chunks = await chunk_code_async(file_docs)
        # logger.info(f"--> Chunked {path} into {len(chunks)} chunks.")

        # Analyze chunks
        analysis_results = await analyze(chunks)

        # Stream results immediately (append mode)
        await stream_jsonline_output_async(analysis_results, output_path)

        logger.info("Streamed results for %s", path)
        queue.task_done()

async def main(num_consumers: int):
    start_time = time.time()
    logger.info("Starting asynchronous code analysis...")

    clone_repo(REPO_URL, REPO_PATH)
    file_paths = await collect_files_async(REPO_PATH)
    # chunks = await chunk_code_async(files)
    # results = await analyze(chunks)
    queue = Queue()
    tasks = [asyncio.create_task(producer(file_paths, queue, num_consumers))]
    for _ in range(num_consumers):
        tasks.append(asyncio.create_task(consumer(queue, OUTPUT_PATH)))

    await asyncio.gather(*tasks)
    # await stream_json_output_async(results, OUTPUT_PATH)
    
    logger.info("Asynchronous code analysis completed.")
    logger.info("Results saved to %s", OUTPUT_PATH)
    logger.info("Total time taken: %s seconds", time.time() - start_time)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--consumers", type=int, default=1,
                        help="Number of consumer tasks (default=1)")
    args = parser.parse_args()
    asyncio.run(main(args.consumers))
