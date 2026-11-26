
from pathlib import Path

# STEP 1: Create the main assignment folder
base_folder = Path(r"C:\Python_Automation\ass9")

# STEP 2: Create the source folder
source_folder = base_folder / "source_files"

# STEP 3: Create subfolders inside source_files
documents_folder = source_folder / "Documents"
images_folder = source_folder / "Images"

documents_folder.mkdir(parents=True, exist_ok=True)
images_folder.mkdir(parents=True, exist_ok=True)

# STEP 4: Create sample text files

(documents_folder / "notes.txt").write_text(
    "These are my important notes.\nThis file is used for backup practice.",
    encoding="utf-8"
)

(documents_folder / "report.txt").write_text(
    "Monthly Sales Report\nTotal Sales: 50000",
    encoding="utf-8"
)

(images_folder / "photo_info.txt").write_text(
    "This is a sample file inside the Images folder.",
    encoding="utf-8"
)

(source_folder / "sales.txt").write_text(
    "Product: Laptop\nQuantity: 5\nPrice: 45000",
    encoding="utf-8"
)

# STEP 5: Create the backups folder
backup_folder = base_folder / "backups"
backup_folder.mkdir(parents=True, exist_ok=True)

print("Folders and sample files created successfully!")
print("Source folder:", source_folder)
print("Backup folder:", backup_folder)
