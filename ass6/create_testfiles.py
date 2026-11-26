
from pathlib import Path
import shutil

# STEP 1: Set the main folder location

base_folder = Path(r"C:\Python_Automation\ass6")

# STEP 2: Create the main testing folder

test_folder = base_folder / "files_to_check"

test_folder.mkdir(parents=True, exist_ok=True)

# STEP 3: Create three subfolders

documents = test_folder / "Documents"
backup = test_folder / "Backup"
old_files = test_folder / "OldFiles"

documents.mkdir(exist_ok=True)
backup.mkdir(exist_ok=True)
old_files.mkdir(exist_ok=True)

# STEP 4: Write sample content

report_content = """This is a sample company report.

The company sells laptops, computers and mobile phones.

The total sales for this month are 500000 rupees.

This report is created to test the Python duplicate file finder program.
"""

notes_content = """Learning Python is interesting.

I am practising file handling and automation.

This is a different file for testing.
"""

# STEP 5: Create the original file

original_file = documents / "report.txt"

original_file.write_text(
    report_content,
    encoding="utf-8"
)

# STEP 6: Create the first duplicate file

first_copy = backup / "report_copy.txt"

shutil.copy2(original_file, first_copy)

# STEP 7: Create the second duplicate file

second_copy = old_files / "document_01.txt"

shutil.copy2(original_file, second_copy)

# STEP 8: Create a different file

notes_file = documents / "notes.txt"

notes_file.write_text(
    notes_content,
    encoding="utf-8"
)

# STEP 9: Display the result

print("Folders and files created successfully!")

print("\nCreated folder structure:")

print("files_to_check/")
print("    Documents/")
print("        report.txt")
print("        notes.txt")
print("    Backup/")
print("        report_copy.txt")
print("    OldFiles/")
print("        document_01.txt")

print("\nThree identical files have been created.")

print("One different file has also been created.")

print("\nYou can now run duplicate_finder.py!")
