
from pathlib import Path

# Automatically find the Python file location
main_folder = Path(__file__).parent

# Automatically create testing folder
folder = main_folder / "Assignment2_Files"
folder.mkdir(exist_ok=True)

# Create sample files
sample_files = [
    "IMG_001.jpg",
    "IMG_002.jpg",
    "IMG_003.jpg",
    "IMG_004.png",
    "IMG_005.png",
    "document.txt"
]

for filename in sample_files:
    file_path = folder / filename

    if not file_path.exists():
        file_path.write_text("This is a sample file.")

print("Sample files created successfully!")

# Get new filename prefix
prefix = input("\nEnter the new filename prefix: ")

# Get starting number
start_number = int(input("Enter starting number (example: 1): "))

# Get file types
print("\nAvailable file types: jpg, png, txt")

extensions = input(
    "Enter extensions to rename separated by commas (example: jpg,png): "
)

selected_extensions = [
    "." + ext.strip().lower().lstrip(".")
    for ext in extensions.split(",")
    if ext.strip()
]

# Find matching files
files = sorted(
    [
        file for file in folder.iterdir()
        if file.is_file()
        and file.suffix.lower() in selected_extensions
    ]
)

# Prepare new filenames
rename_list = []

number = start_number

for file in files:

    new_name = f"{prefix}_{number:03d}{file.suffix}"

    new_path = folder / new_name

    rename_list.append((file, new_path))

    number += 1

# Preview filenames
print("\n========== PREVIEW ==========")

for old_file, new_file in rename_list:
    print(old_file.name, " ---> ", new_file.name)

# Ask for confirmation
choice = input("\nDo you want to rename these files? (yes/no): ")

if choice.lower() == "yes":

    print("\n========== RENAMING FILES ==========")

    for old_file, new_file in rename_list:

        # Prevent overwriting existing files
        if old_file == new_file:
            print("Already has this name:", old_file.name)

        elif new_file.exists():
            print("Skipped because name already exists:", new_file.name)

        else:
            old_file.rename(new_file)

            print("Renamed:", old_file.name, "to", new_file.name)

    print("\nRenaming completed!")

else:
    print("\nRenaming cancelled!")
