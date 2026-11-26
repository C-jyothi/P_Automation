
# STEP 1: Import required modules

import zipfile
import shutil
import logging

from pathlib import Path
from datetime import datetime


# STEP 2: Set folder locations

base_folder = Path(r"C:\Python_Automation\ass9")

source_folder = base_folder / "source_files"
backup_folder = base_folder / "backups"


# STEP 3: Set the maximum number of backups

MAX_BACKUPS = 3


# STEP 4: Create the backup folder if it does not exist

backup_folder.mkdir(parents=True, exist_ok=True)


# STEP 5: Set up logging

log_file = backup_folder / "backup_log.txt"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)


# STEP 6: Create the backup

def create_backup():

    try:

        # Check whether the source folder exists

        if not source_folder.exists():

            print("Source folder does not exist!")
            logging.error("Source folder does not exist.")
            return

        # Get the current date and time

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Create the ZIP file name

        zip_name = f"backup_{current_time}.zip"

        zip_path = backup_folder / zip_name

        # Count the files to be backed up

        files = [file for file in source_folder.rglob("*") if file.is_file()]

        if not files:
            print("Source folder is empty!")
            logging.warning("Source folder is empty.")
            return

        # Check available disk space

        total_size = sum(file.stat().st_size for file in files)

        free_space = shutil.disk_usage(backup_folder).free

        if free_space < total_size:
            print("Not enough free disk space for this backup!")
            logging.error("Insufficient disk space.")
            return

        # Create a ZIP archive

        with zipfile.ZipFile(
            zip_path,
            "w",
            compression=zipfile.ZIP_DEFLATED
        ) as zip_file:

            for file in files:

                # Keep the folder structure inside the ZIP

                relative_path = file.relative_to(source_folder)

                zip_file.write(file, relative_path)

        print("Backup created successfully!")
        print("Backup file:", zip_path)

        logging.info(f"Backup created successfully: {zip_name}")

        # STEP 7: Remove older backups if the limit is exceeded

        manage_old_backups()

    except OSError as error:

        print("File or storage error:", error)
        logging.error(f"File or storage error: {error}")

    except Exception as error:

        print("An unexpected error occurred:", error)
        logging.exception("Unexpected error occurred.")


# STEP 8: Manage old backup versions

def manage_old_backups():

    # Find all ZIP backup files

    backup_files = sorted(
        backup_folder.glob("backup_*.zip"),
        key=lambda file: file.stat().st_mtime,
        reverse=True
    )

    # Keep only the newest MAX_BACKUPS files

    old_backups = backup_files[MAX_BACKUPS:]

    for old_file in old_backups:

        old_file.unlink()

        print("Old backup deleted:", old_file.name)

        logging.info(f"Old backup deleted: {old_file.name}")


# STEP 9: Run the backup program

create_backup()
