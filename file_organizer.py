
from pathlib import Path
import shutil

# STEP 1: Define file categories

file_categories = {
    "Documents": [".pdf", ".doc", ".docx", ".ppt", ".pptx"],

    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],

    "Spreadsheets": [".xls", ".xlsx", ".xlsm", ".csv"],

    "Text Files": [".txt", ".log", ".md"],

    "Programs": [".py", ".java", ".c", ".cpp", ".js", ".html", ".css"],

    "Others": []
}


# STEP 2: Find the correct category

def get_category(file):

    extension = file.suffix.lower()

    for category, extensions in file_categories.items():

        if extension in extensions:
            return category

    return "Others"


# STEP 3: Avoid overwriting files

def get_unique_destination(destination):

    if not destination.exists():
        return destination

    counter = 1

    while True:

        new_name = (
            destination.stem
            + "_"
            + str(counter)
            + destination.suffix
        )

        new_destination = destination.with_name(new_name)

        if not new_destination.exists():
            return new_destination

        counter += 1


# STEP 4: Get folder path from the user

folder_path = input("Enter the folder path to organise: ").strip()

folder = Path(folder_path.strip('"')).expanduser()


# STEP 5: Check whether the folder exists

if not folder.exists() or not folder.is_dir():

    print("Error: The specified folder does not exist.")

else:

    # Store the number of moved files in each category

    file_count = {
        category: 0
        for category in file_categories
    }

    failed_count = 0

    # STEP 6: Create category folders if necessary

    try:

        for category in file_categories:

            destination_folder = folder / category

            destination_folder.mkdir(exist_ok=True)

        # STEP 7: Find all files in the selected folder

        files = [
            item for item in folder.iterdir()
            if item.is_file()
        ]

        # STEP 8: Move files into the correct folders

        for file in files:

            try:

                category = get_category(file)

                destination_folder = folder / category

                destination = destination_folder / file.name

                # Generate a new name if the file already exists

                destination = get_unique_destination(destination)

                # Move the file

                shutil.move(str(file), str(destination))

                file_count[category] += 1

                print(f"Moved: {file.name} -> {category}")

            except (OSError, shutil.Error) as error:

                failed_count += 1

                print(f"Could not move {file.name}: {error}")

        # STEP 9: Display the final summary

        print("\n========== ORGANISATION SUMMARY ==========")

        for category, count in file_count.items():

            print(f"{category}: {count} files")

        print(f"Failed files: {failed_count}")

        print("==========================================")

    except OSError as error:

        print("Folder operation failed:", error)
