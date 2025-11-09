# Async Code Chunker

This project implements an async-safe, overlap-aware code chunking pipeline using Tree-sitter and LangChain's `RecursiveCharacterTextSplitter`. It’s designed for scalable LLM preprocessing and includes test coverage.

## Features

- flexible LLM model and analyser can be loaded over env variables
- Token- and character-aware splitting with overlap
- Async-safe pipeline using `asyncio.gather`
- Modular design with per-file metadata
- Unit tests with `pytest-asyncio`

## Project Structure

- src/ingest/clone_repo.py #clone repo
- src/ingest/file_loader.py #load files
- src/processing/chunker.py #Async chunk
- src/llm/analyser_google.py #LLM google
- src/llm/analyser_openai.py #LLM openai

## Install dependencies
pip install -r requirements.txt

## Run
python main.py

## Run tests
pytest tests/