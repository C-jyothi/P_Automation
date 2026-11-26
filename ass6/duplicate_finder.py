
import hashlib
import csv
from pathlib import Path


# STEP 1: Specify the folder to check

folder_path = Path(
    r"C:\Python_Automation\ass6\files_to_check"
)

# Save the report in the ass6 folder
output_file = folder_path.parent / "duplicate_report.csv"


# STEP 2: Create a function to calculate file hash

def calculate_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while True:

            data = file.read(4096)

            if not data:

                break

            sha256.update(data)

    return sha256.hexdigest()


# STEP 3: Check whether the folder exists

if not folder_path.exists():

    print("The folder does not exist.")

else:

    # STEP 4: Create a dictionary to store files

    file_groups = {}

    error_count = 0

    # STEP 5: Scan all files and subfolders

    for file_path in folder_path.rglob("*"):

        if file_path.is_file():

            try:

                file_hash = calculate_hash(file_path)

                if file_hash in file_groups:

                    file_groups[file_hash].append(file_path)

                else:

                    file_groups[file_hash] = [file_path]

            except Exception as error:

                error_count += 1

                print("Could not read:", file_path)
                print("Reason:", error)


    # STEP 6: Find duplicate files

    duplicate_groups = []

    for file_hash, files in file_groups.items():

        if len(files) > 1:

            duplicate_groups.append(files)


    # STEP 7: Prepare report information

    total_duplicate_groups = len(duplicate_groups)

    total_duplicate_copies = 0

    total_space_saved = 0

    report_data = []


    # STEP 8: Display duplicate information

    if total_duplicate_groups == 0:

        print("\nNo duplicate files found.")

    else:

        print("\nDuplicate files found!")

        for group_number, files in enumerate(
            duplicate_groups, start=1
        ):

            file_size = files[0].stat().st_size

            size_mb = file_size / (1024 * 1024)

            duplicate_copies = len(files) - 1

            space_saved = file_size * duplicate_copies

            space_saved_mb = space_saved / (1024 * 1024)

            total_duplicate_copies += duplicate_copies

            total_space_saved += space_saved

            print("\nDuplicate Group:", group_number)

            for file_path in files:

                print("File:", file_path)

                report_data.append([
                    group_number,
                    str(file_path),
                    file_size,
                    round(size_mb, 2),
                    duplicate_copies,
                    round(space_saved_mb, 2)
                ])

            print("File Size:", round(size_mb, 2), "MB")

            print("Duplicate Copies:", duplicate_copies)

            print(
                "Potential Space Savings:",
                round(space_saved_mb, 2),
                "MB"
            )


    # STEP 9: Create CSV report

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "Duplicate Group",
            "File Path",
            "File Size (Bytes)",
            "File Size (MB)",
            "Duplicate Copies",
            "Potential Space Savings (MB)"
        ])

        writer.writerows(report_data)


    # STEP 10: Display final summary

    print("\n========== FINAL SUMMARY ==========")

    print("Total Files Scanned:", sum(
        len(files) for files in file_groups.values()
    ))

    print("Duplicate Groups:", total_duplicate_groups)

    print("Duplicate Copies:", total_duplicate_copies)

    print(
        "Total Potential Space Savings:",
        round(total_space_saved / (1024 * 1024), 2),
        "MB"
    )

    print("Files That Could Not Be Read:", error_count)

    print("\nCSV Report Created Successfully!")

    print("Report Location:", output_file)
