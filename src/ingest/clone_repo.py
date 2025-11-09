from git import Repo
import os
from src.utils.logger import setup_logger
logger = setup_logger()

def clone_repo(dest_url: str, dest_path: str):
    if not os.path.exists(dest_path):
        logger.info(f"Cloning code into {dest_path}...")
        Repo.clone_from(dest_url, dest_path)
    else:
        logger.info(f"Repository already exists at {dest_path}. Skipping clone.")
