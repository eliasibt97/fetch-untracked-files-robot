import os
import re
from dotenv import load_dotenv
from pathlib import Path
from ftplib import FTP
from logger import setup_logger

load_dotenv()

logger = setup_logger()
logger.info("Starting app...")

assets_path = os.getenv("ASSETS_PATH")

if not assets_path:
  logger.error("ASSETS_PATH environment variable is not set")
  raise ValueError("ASSETS_PATH environment variable is not set")

logger.info("Verifying assets path...")
index_file_path = Path(assets_path) / "index.txt"

if not index_file_path.exists() or not index_file_path.is_file():
  logger.error(f"index.txt file not found in {assets_path}")
  raise FileNotFoundError(f"index.txt file not found in {assets_path}")

paths = []
modified_pattern = re.compile(r"modified:\s+(.+)")

logger.info("Reading index.txt file...")
with open(index_file_path, "r") as index_file:
  for line in index_file:
    line = line.strip()
    match = modified_pattern.search(line)
    if match:
      paths.append(match.group(1))
    else:
      paths.append(line)

logger.info(f"Found {len(paths)} paths to fetch")
logger.info(f"Paths to fetch: {paths}")

# TODO: Pending to implement root directories for master ("/") and development ("dev.sistemaclubice.net")
ENV = os.getenv("ENV")

logger.info("Connecting to FTP server...")
local_path = os.getenv("LOCAL_FILES_PATH")
ftp_server = os.getenv("FTP_SERVER")
ftp_user = os.getenv("FTP_USER")
ftp_password = os.getenv("FTP_PASSWORD")

with FTP(ftp_server) as ftp:
  ftp.login(ftp_user, ftp_password)
  logger.info("Connected to FTP server. Moving to root directory.")
  ftp.cwd('/')
  for path in paths:
    directory, filename = path.rsplit('/', 1)
    ftp.cwd(directory)

    logger.info(f"Fetching {filename} from {directory}")

    local_file = Path(local_path) / path
    local_file.parent.mkdir(parents=True, exist_ok=True)

    with open(local_file, 'wb') as f:
      logger.info(f"Retrieving {filename} from FTP server, and updating local file in local path")
      ftp.retrbinary(f'RETR {filename}', f.write)  
    ftp.cwd('/')
    
logger.info("Finished fetching files")
  
          