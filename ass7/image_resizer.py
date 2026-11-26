
from pathlib import Path
from PIL import Image
import csv


# STEP 1: Set folder locations

base_folder = Path(r"C:\Python_Automation\ass7")

input_folder = base_folder / "input_images"

output_folder = base_folder / "output_images"


# STEP 2: Set resizing options

target_width = 800

target_height = 600

output_format = "JPEG"

jpeg_quality = 85


# STEP 3: Create output folder if it does not exist

output_folder.mkdir(parents=True, exist_ok=True)


# STEP 4: Find supported image files

supported_formats = [
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp"
]

image_files = []

for file in input_folder.iterdir():

    if file.is_file() and file.suffix.lower() in supported_formats:

        image_files.append(file)


# STEP 5: Create a list to store report information

report_data = []


# STEP 6: Process each image

for file_path in image_files:

    try:

        # Open the original image
        image = Image.open(file_path)

        # Get original dimensions
        original_width, original_height = image.size

        # Get original file size in KB
        original_size = file_path.stat().st_size / 1024

        # STEP 7: Resize while maintaining aspect ratio

        image.thumbnail((target_width, target_height))

        # Get resized dimensions
        new_width, new_height = image.size

        # STEP 8: Select output format

        if output_format == "JPEG":

            # JPEG does not support transparency
            image = image.convert("RGB")

            extension = ".jpg"

        else:

            if image.mode not in ("RGB", "RGBA"):

                image = image.convert("RGBA")

            extension = ".png"

        # STEP 9: Create output filename

        output_name = file_path.stem + extension

        output_path = output_folder / output_name

        # STEP 10: Save the resized image

        if output_format == "JPEG":

            image.save(
                output_path,
                format="JPEG",
                quality=jpeg_quality
            )

        else:

            image.save(
                output_path,
                format="PNG"
            )

        # Get resized file size
        new_size = output_path.stat().st_size / 1024

        # STEP 11: Store report information

        report_data.append([
            file_path.name,
            original_width,
            original_height,
            round(original_size, 2),
            output_name,
            new_width,
            new_height,
            round(new_size, 2)
        ])

        print("\nProcessed:", file_path.name)

        print(
            "Original dimensions:",
            original_width,
            "x",
            original_height
        )

        print(
            "New dimensions:",
            new_width,
            "x",
            new_height
        )

        print("Image saved successfully!")

    except Exception as error:

        print("\nCould not process:", file_path.name)

        print("Reason:", error)


# STEP 12: Generate CSV report

report_file = base_folder / "image_report.csv"

with open(
    report_file,
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    writer = csv.writer(csv_file)

    writer.writerow([
        "Original File",
        "Original Width",
        "Original Height",
        "Original Size (KB)",
        "Output File",
        "New Width",
        "New Height",
        "New Size (KB)"
    ])

    writer.writerows(report_data)


# STEP 13: Display final summary

print("\n---------- FINAL SUMMARY ----------")

print("Total images found:", len(image_files))

print("Successfully processed:", len(report_data))

print("Output format:", output_format)

print("Target maximum width:", target_width)

print("Target maximum height:", target_height)

print("\nResized images saved at:", output_folder)

print("Report saved at:", report_file)

print("\nImage resizing completed!")
