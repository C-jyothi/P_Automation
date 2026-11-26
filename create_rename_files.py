from pathlib import Path

# Ask for folder name
folder_name = input("Enter folder name: ")

# Get the current working directory
current_folder = Path.cwd()

# Combine current folder and entered folder name
folder_path = current_folder / folder_name

# Check whether folder exists
if not folder_path.exists():
    print("Folder does not exist!")
    exit()

if not folder_path.is_dir():
    print("The given name is not a folder!")
    exit()

print("Selected folder:", folder_path)