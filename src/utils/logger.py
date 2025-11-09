import logging

def setup_logger(name="peersland"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        file_handler = logging.FileHandler("peerland.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
