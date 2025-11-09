# Async Code Chunker

This project implements an async-safe, overlap-aware code chunking pipeline using Tree-sitter and LangChain's `RecursiveCharacterTextSplitter`. It’s designed for scalable LLM preprocessing and includes test coverage.

## Approach

This project implements an async-safe, scalable code chunking pipeline designed for preprocessing source code before LLM analysis. The pipeline is modular, testable, and optimized for performance and reproducibility.

## Methodology

- Async file collection: Uses asyncio to traverse and read files concurrently, improving I/O throughput.
- Chunking with LangChain: Applies RecursiveCharacterTextSplitter to split code into context-preserving chunks using newline and token-aware heuristics.
- Parallel chunking: Leverages asyncio.gather() to chunk multiple files concurrently, reducing latency across large repositories.
- Metadata preservation: Each chunk retains its source file path for traceability and downstream filtering.
- Batch-safe analysis: Supports batching of chunks for efficient LLM interaction, with configurable batch size to manage rate limits and memory.

## Best Practice

- Each pipeline stage (collection, chunking, analysis, streaming) is independently testable and reusable.

## Limitation

- Current implementation uses character-based splitting and does not parse language-specific syntax.
- Structural parsing via Tree-sitter is not implemented but can be added to improve semantic chunking (e.g: function-level splits).
- (Tried to implement it. Unable to finish on time)
- Designed for one repository at a time; multi-repo or monorepo support can be added.

## To do

- AST-based chunking for language-aware splits (e.g: functions, classes).
- API keys are save in env file for ease of testing. In production it should be moved to secrets.

## Features

- flexible LLM model and analyser can be loaded over env variables
- Token- and character-aware splitting with overlap
- Async-safe pipeline using `asyncio.gather`
- Modular design with per-file metadata
- Unit tests with `pytest-asyncio`

## Project Structure

- src/ingest/clone_repo.py 'clone repo'
- src/ingest/file_loader.py 'load files'
- src/processing/chunker.py 'Async chunk'
- src/llm/analyser_google.py 'LLM google'
- src/llm/analyser_openai.py 'LLM openai'

## Install dependencies
pip install -r requirements.txt

## Run
python main.py

## Run tests
pytest tests/