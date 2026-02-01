# Fetch Untracked Files Robot

> A small utility to fetch files listed in an index from a remote FTP server and save them to a local path.

## Overview

This project reads a list of paths from `assets/index.txt` and downloads each file from a configured FTP server into a local directory, preserving relative paths.

Key behavior is implemented in [app.py](app.py) and logging is initialized in [logger.py](logger.py).

## Files
- [app.py](app.py): Main script that reads `index.txt`, connects to the FTP server, and downloads files.
- [logger.py](logger.py): Logger setup used by the app.
- assets/index.txt: Input file with file paths (or lines containing `modified: <path>`).
- logs/: Directory where runtime logs are written.

## Requirements
- Python 3.8+
- `python-dotenv` (optional but recommended for loading `.env` variables)

Install with pip if needed:

```bash
pip install python-dotenv
```

## Environment

The app reads configuration from environment variables (you can place them in a `.env` file):

- `ASSETS_PATH` — path to the `assets` folder (required).
- `LOCAL_FILES_PATH` — local base path where downloaded files are saved (required).
- `FTP_SERVER` — host or IP of the FTP server (required).
- `FTP_USER` — FTP username (required).
- `FTP_PASSWORD` — FTP password (required).
- `MAIN_REMOTE_PATH` — FTP remote base path to `cwd` into before downloading (required).

Example `.env`:

```
ASSETS_PATH=assets
LOCAL_FILES_PATH=local_files
FTP_SERVER=ftp.example.com
FTP_USER=ftpuser
FTP_PASSWORD=secret
MAIN_REMOTE_PATH=/path/on/server
```

## index.txt format

Each line in `assets/index.txt` should reference a file path relative to the remote base. Lines can be plain paths or include `modified: <path>`; the script extracts the path in either case.

Examples:

```
folder/subfolder/file1.txt
modified: folder/other/file2.txt
```

## Usage

1. Ensure environment variables are set (or create a `.env` file).
2. Put `index.txt` into the directory pointed to by `ASSETS_PATH` (default example is `assets/index.txt`).
3. Run the script:

```bash
python app.py
```

Downloaded files are saved under `LOCAL_FILES_PATH`, preserving the relative structure from the index.

## Logging

Logs are produced by the logger in [logger.py](logger.py) and can be found in the `logs/` folder.

## Troubleshooting

- If `ASSETS_PATH` is not set or `assets/index.txt` is missing, the script will raise an error.
- Ensure FTP credentials and `MAIN_REMOTE_PATH` are correct and the FTP user has permission to read the referenced files.

---
Made with ❤️ by [Eliasib Toris](https://github.com/eliasibt97/).
