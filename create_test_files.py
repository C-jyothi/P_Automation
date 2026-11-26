
from pathlib import Path

# Create TestFiles folder
folder = Path(__file__).parent / "TestFiles"

folder.mkdir(exist_ok=True)

# Sample file names
sample_files = [
    "report.pdf",
    "photo.jpg",
    "sales.xlsx",
    "notes.txt",
    "script.py",
    "archive.zip"
]

# Create the sample files
for file_name in sample_files:

    file_path = folder / file_name

    if not file_path.exists():
        file_path.touch()
        print("Created:", file_name)

    else:
        print("Already exists:", file_name)

print("\nAll sample files are ready!")
print("Folder location:", folder.resolve())
