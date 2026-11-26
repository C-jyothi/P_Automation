
import shutil
import time
import logging
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# STEP 1: Set the folder locations

base_folder = Path(r"C:\Python_Automation\ass5")

incoming_folder = base_folder / "incoming"

processed_folder = base_folder / "processed"


# STEP 2: Create folders if they do not exist

base_folder.mkdir(parents=True, exist_ok=True)
incoming_folder.mkdir(parents=True, exist_ok=True)
processed_folder.mkdir(parents=True, exist_ok=True)


# STEP 3: Create a log file

logging.basicConfig(
    filename=str(base_folder / "processing.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


# STEP 4: Define file categories

file_categories = {

    "Documents": [".pdf", ".doc", ".docx"],

    "Spreadsheets": [".xlsx", ".xls", ".csv"],

    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],

    "Text Files": [".txt"],

    "Programs": [".py", ".exe", ".bat"]

}


# STEP 5: Identify the file category

def get_category(file_path):

    extension = file_path.suffix.lower()

    for category, extensions in file_categories.items():

        if extension in extensions:

            return category

    return "Others"


# STEP 6: Wait until the file is completely copied

def wait_until_ready(file_path):

    previous_size = None

    stable_count = 0

    for attempt in range(30):

        if not file_path.exists():

            return False

        current_size = file_path.stat().st_size

        if current_size == previous_size:

            stable_count = stable_count + 1

        else:

            stable_count = 0

        if stable_count >= 3:

            return True

        previous_size = current_size

        time.sleep(1)

    return False


# STEP 7: Avoid overwriting files with the same name

def get_unique_path(destination):

    counter = 1

    new_destination = destination

    while new_destination.exists():

        new_name = (
            destination.stem
            + "_"
            + str(counter)
            + destination.suffix
        )

        new_destination = destination.with_name(new_name)

        counter = counter + 1

    return new_destination


# STEP 8: Create a class to monitor new files

class FolderHandler(FileSystemEventHandler):

    def __init__(self):

        self.processed_files = set()

    def on_created(self, event):

        # Ignore folders
        if event.is_directory:

            return

        file_path = Path(event.src_path)

        file_key = str(file_path.resolve())

        # Avoid processing the same file twice
        if file_key in self.processed_files:

            return

        self.processed_files.add(file_key)

        print("\nNew file detected:", file_path.name)

        try:

            # Wait until copying is completed
            if not wait_until_ready(file_path):

                print("File is not ready:", file_path.name)

                self.processed_files.discard(file_key)

                return

            # Find the file category
            category = get_category(file_path)

            # Create the destination folder
            category_folder = processed_folder / category

            category_folder.mkdir(parents=True, exist_ok=True)

            # Create the destination file path
            destination = category_folder / file_path.name

            # Avoid overwriting existing files
            destination = get_unique_path(destination)

            # Move the file
            shutil.move(str(file_path), str(destination))

            # Save the activity in the log
            logging.info(
                "Processed: %s -> %s",
                file_path.name,
                destination
            )

            print("File moved successfully!")
            print("Category:", category)

        except Exception as error:

            logging.error(
                "Could not process %s: %s",
                file_path.name,
                error
            )

            print("Error processing file:", error)


# STEP 9: Start monitoring the folder

event_handler = FolderHandler()

observer = Observer()

observer.schedule(
    event_handler,
    str(incoming_folder),
    recursive=False
)

observer.start()

print("Folder monitoring started!")
print("Watching folder:", incoming_folder)

print("Add files to the incoming folder.")
print("Press Ctrl + C to stop monitoring.")


# STEP 10: Keep the program running

try:

    while True:

        time.sleep(1)

except KeyboardInterrupt:

    print("\nStopping folder monitoring...")

    observer.stop()

observer.join()

print("Folder monitoring stopped.")
