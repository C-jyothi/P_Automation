
import shutil
from pathlib import Path

# Get the location of this Python file
main_folder = Path(__file__).parent

# Automatically create a testing folder
source_folder = main_folder / "Assignment1_Files"

source_folder.mkdir(exist_ok=True)

# Create sample files automatically
sample_files = {
    "report.pdf": "This is a sample PDF document.",
    "notes.docx": "This is a sample Word document.",
    "photo.jpg": "This is a sample image.",
    "logo.png": "This is another sample image.",
    "sales.xlsx": "This is a sample Excel file.",
    "notes.txt": "This is a sample text file.",
    "script.py": "print('Hello World')",
    "archive.zip": "This is a sample ZIP file."
}

# Create the sample files
for filename, content in sample_files.items():
    file_path = source_folder / filename

    if not file_path.exists():
        file_path.write_text(content)

print("Sample files created successfully!")

# Define file categories
file_categories = {
    "Documents": [".pdf", ".doc", ".docx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Text Files": [".txt"],
    "Programs": [".py", ".java", ".cpp"],
    "Others": []
}

# Count moved files
file_count = {
    category: 0 for category in file_categories
}

# Organise files
for file in source_folder.iterdir():

    if file.is_file():

        extension = file.suffix.lower()

        destination_category = "Others"

        # Identify the correct category
        for category, extensions in file_categories.items():

            if extension in extensions:
                destination_category = category
                break

        # Create destination folder
        destination_folder = source_folder / destination_category
        destination_folder.mkdir(exist_ok=True)

        # Avoid overwriting existing files
        destination_file = destination_folder / file.name

        counter = 1

        while destination_file.exists():
            destination_file = destination_folder / (
                f"{file.stem}_{counter}{file.suffix}"
            )
            counter += 1

        try:
            shutil.move(str(file), str(destination_file))

            file_count[destination_category] += 1

            print("Moved:", file.name, "to", destination_category)

        except Exception as e:
            print("Could not move:", file.name)
            print("Reason:", e)

# Display summary
print("\n========== ORGANISING SUMMARY ==========")

for category, count in file_count.items():
    print(category, ":", count, "files")

print("\nFile organisation completed!")
