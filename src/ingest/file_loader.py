import os
import asyncio
import aiofiles
from src.config import (SUPPORTED_FILE_TYPES)
from src.utils.logger import setup_logger
logger = setup_logger()

def collect_code_files(root_dir: str):
    code_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(tuple(SUPPORTED_FILE_TYPES)):
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code_files.append((file_path, f.read()))
                    logger.info(f"Stopping after first code file {file} in directory.")
                except Exception as e:
                    logger.info(f"Error reading {file}: {e}")
                break  # stop after first match in this directory
        if len(code_files) > 3:  # Limit total files for testing
            break  # stop after first file overall
    return [{"path": p, "content": c} for p, c in code_files]


async def read_file_async(path):
    async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
        return await f.read()

async def collect_code_files_async(repo_path, extensions=SUPPORTED_FILE_TYPES):
    file_paths = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                logger.info(f"Found code file: {file}")
                file_paths.append(os.path.join(root, file))

    contents = await asyncio.gather(*(read_file_async(p) for p in file_paths))
    return [{"path": p, "content": c} for p, c in zip(file_paths, contents)]

async def collect_files_async(repo_path, extensions=SUPPORTED_FILE_TYPES):
    file_paths = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                logger.info(f"Found code file: {file}")
                file_paths.append(os.path.join(root, file))
                # if file_paths:
                #     break  # Stop after first match in this directory
        # if file_paths:
        #     break  # Stop after first file overall

    return file_paths
