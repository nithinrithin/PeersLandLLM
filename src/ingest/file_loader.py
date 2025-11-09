import os
import asyncio
import aiofiles
from src.config import (SUPPORTED_FILE_TYPES)
from src.utils.logger import setup_logger
logger = setup_logger()

def collect_code_files(root_dir: str):
    code_files = []
    for root, _, files in os.walk(root_dir):
        # This count ensures we only take the first code file
        count = 0 
        for file in files:
            if file.endswith(tuple(SUPPORTED_FILE_TYPES)):
                count += 1
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        code_files.append(f.read())
                except Exception as e:
                    logger.info(f"Error reading {file}: {e}")
            if count == 1:
                logger.info(f"Stoping after first code file {file} in directory.")
                break
        if count == 1:
            logger.info("Stoping after first code file")
            break
    return code_files

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
