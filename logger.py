import logging
from datetime import datetime
from pathlib import Path

def setup_logger():
  logger = logging.getLogger('main_logger')
  logger.setLevel(logging.DEBUG)

  timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
  log_path = Path("logs")
  log_full_path = log_path / f"{timestamp}-logs.log"
  log_path.mkdir(parents=True, exist_ok=True)
  handler = logging.FileHandler(log_full_path)

  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  return logger
  