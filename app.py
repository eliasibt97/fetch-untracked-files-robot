import os
import re
from dotenv import load_dotenv
from pathlib import Path
from ftplib import FTP
from logger import setup_logger
from datetime import datetime

load_dotenv()

logger = setup_logger()
logger.info("Starting app...")

inputs_path = Path(os.getenv("INPUTS_PATH"))
processed_path = Path(os.getenv("OUTPUTS_PATH"))
processed_path.mkdir(parents=True, exist_ok=True)

logger.info("Verifying inputs path...")
if not inputs_path:
  logger.error("INPUTS_PATH environment variable is not set")
  raise ValueError("INPUTS_PATH environment variable is not set")

if not os.path.isdir(inputs_path):
  logger.error(f"The inputs path {inputs_path} is not a directory")
  raise ValueError(f"The inputs path {inputs_path} is not a directory")

if not any(Path(inputs_path).iterdir()):
  logger.error(f"The inputs path {inputs_path} is empty")
  raise ValueError(f"The inputs path {inputs_path} is empty")

paths = []
modified_pattern = re.compile(r"modified:\s+(.+)")

logger.info("Reading index.txt file...")
for txt_file in inputs_path.glob("*.txt"):
  logger.info(f"Reading {txt_file}")

  with txt_file.open() as index_file:
    logger.info(f"Reading {txt_file}")
    for line in index_file:
      line = line.strip()
      if not line:
        continue

      match = modified_pattern.search(line)
      if match:
        paths.append(match.group(1))
      else:
        paths.append(line)    
  logger.info("Removing processed input .txt files")
  txt_file.unlink()

if len(paths) == 0:
  logger.error("No paths found in the inputs path")
  raise ValueError("No paths found in the inputs path")

paths = list(dict.fromkeys(paths))

logger.info(f"Found {len(paths)} paths to fetch")
logger.info(f"Paths to fetch: {paths}")

logger.info("Connecting to FTP server...")
local_path = os.getenv("LOCAL_FILES_PATH")
ftp_server = os.getenv("FTP_SERVER")
ftp_user = os.getenv("FTP_USER")
ftp_password = os.getenv("FTP_PASSWORD")

remote_path = os.getenv("MAIN_REMOTE_PATH")

with FTP(ftp_server) as ftp:
  ftp.login(ftp_user, ftp_password)
  logger.info("Connected to FTP server. Moving to root directory.")
  ftp.cwd(f"{remote_path}")
  for path in paths:
    directory, filename = path.rsplit('/', 1)
    ftp.cwd(directory)

    logger.info(f"Fetching {filename} from {directory}")

    local_file = Path(local_path) / path
    local_file.parent.mkdir(parents=True, exist_ok=True)

    with open(local_file, 'wb') as f:
      logger.info(f"Retrieving {filename} from FTP server, and updating local file in local path")
      ftp.retrbinary(f'RETR {filename}', f.write)  
    ftp.cwd(f"{remote_path}")

logger.info("Finished fetching files")
    
logger.info("Generating processed file...")
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
processed_file = processed_path / f"processed_{timestamp}.txt"
with processed_file.open("w") as processed_file:
  for path in paths:
    processed_file.write(f"{path}\n")
  processed_file.write(f"Processed at {timestamp}")

logger.info("Finished generating processed file")
logger.info("Finished app")

  
          