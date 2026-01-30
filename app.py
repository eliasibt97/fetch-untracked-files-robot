import os
import re
from dotenv import load_dotenv
from pathlib import Path
from ftplib import FTP

load_dotenv()

assets_path = os.getenv("ASSETS_PATH")
if not assets_path:
  raise ValueError("ASSETS_PATH environment variable is not set")

index_file_path = Path(assets_path) / "index.txt"

if not index_file_path.exists() or not index_file_path.is_file():
  raise FileNotFoundError(f"index.txt file not found in {assets_path}")

paths = []
modified_pattern = re.compile(r"modified:\s+(.+)")

with open(index_file_path, "r") as index_file:
  for line in index_file:
    line = line.strip()
    match = modified_pattern.search(line)
    if match:
      paths.append(match.group(1))
    else:
      paths.append(line)


ENV = os.getenv("ENV")

local_path = os.getenv("LOCAL_FILES_PATH")
ftp_server = os.getenv("FTP_SERVER")
ftp_user = os.getenv("FTP_USER")
ftp_password = os.getenv("FTP_PASSWORD")

with FTP(ftp_server) as ftp:
  ftp.login(ftp_user, ftp_password)
  ftp.cwd('/')
  for path in paths:
    directory, filename = path.rsplit('/', 1)
    ftp.cwd(directory)

    local_file = Path(local_path) / filename
    local_file.parent.mkdir(parents=True, exist_ok=True)

    with open(local_file, 'wb') as f:
      ftp.retrbinary(f'RETR {filename}', f.write)
    ftp.cwd('/')
    
  
          