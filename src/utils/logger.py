import logging
import os

def setup_logging(log_file: str = 'renderer.log') -> None:
    """Setup simple logging to a single file."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_file
    ) 