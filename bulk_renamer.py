
from pathlib import Path


# STEP 1: Get folder path

folder_path = input("Enter folder path: ").strip()

folder = Path(folder_path.strip('"')).expanduser()


# STEP 2: Check folder

if not folder.exists() or not folder.is_dir():

    print("Error: Folder does not exist.")

else:

    # STEP 3: Get prefix

    prefix = input("Enter new filename prefix: ").strip()

    if not prefix:

        print("Error: Prefix cannot be empty.")

    else:

        # STEP 4: Get starting number

        try:

            start_number = int(input("Enter starting number: "))

            if start_number < 0:
                raise ValueError

        except ValueError:

            print("Please enter a valid non-negative number.")

            raise SystemExit

        # STEP 5: Get file types

        print("\nAvailable file types:")
        print(".jpg, .jpeg, .png, .txt, .pdf, .xlsx, .py")

        file_types = input(
            "Enter extensions separated by commas (example: .jpg,.png): "
        )

        extensions = [
            ext.strip().lower()
            for ext in file_types.split(",")
            if ext.strip()
        ]

        # STEP 6: Find matching files

        files = sorted(
            [
                file for file in folder.iterdir()
                if file.is_file()
                and file.suffix.lower() in extensions
            ],
            key=lambda file: file.name.lower()
        )

        if not files:

            print("No matching files found.")

        else:

            # STEP 7: Prepare new filenames

            rename_list = []

            for index, file in enumerate(files):

                number = start_number + index

                new_name = f"{prefix}_{number:03d}{file.suffix}"

                new_path = folder / new_name

                rename_list.append((file, new_path))

            # STEP 8: Preview filenames

            print("\n========== PREVIEW ==========")

            for old_file, new_file in rename_list:

                print(old_file.name, "->", new_file.name)

            print("=============================")

            # STEP 9: Check for existing filenames

            planned_paths = [
                new_path for old_file, new_path in rename_list
            ]

            if len(set(planned_paths)) != len(planned_paths):

                print("Error: Duplicate new filenames found.")

            elif any(
                new_path.exists()
                and new_path not in [old_file for old_file, new_file in rename_list]
                for old_file, new_path in rename_list
            ):

                print("Error: A destination filename already exists.")
                print("No files were renamed.")

            else:

                # STEP 10: Ask permission

                choice = input(
                    "\nDo you want to apply these changes? (yes/no): "
                ).strip().lower()

                if choice == "yes":

                    try:

                        # First rename to temporary names
                        # This avoids conflicts between selected files.

                        temporary_list = []

                        for index, (old_file, new_file) in enumerate(rename_list):

                            temporary_path = folder / f"__temp_rename_{index}__"

                            old_file.rename(temporary_path)

                            temporary_list.append(
                                (temporary_path, new_file)
                            )

                        # Now rename to final filenames

                        for temporary_file, new_file in temporary_list:

                            temporary_file.rename(new_file)

                            print("Renamed:", new_file.name)

                        print("\nAll files renamed successfully!")

                    except OSError as error:

                        print("Renaming error:", error)

                else:

                    print("\nRenaming cancelled.")
