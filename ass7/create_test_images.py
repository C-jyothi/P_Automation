
from pathlib import Path
from PIL import Image, ImageDraw

# STEP 1: Set the main folder path

base_folder = Path(r"C:\Python_Automation\ass7")

# STEP 2: Create input and output folders

input_folder = base_folder / "input_images"
output_folder = base_folder / "output_images"

input_folder.mkdir(parents=True, exist_ok=True)
output_folder.mkdir(parents=True, exist_ok=True)

# STEP 3: Create sample images

image_details = [
    ("mountain.jpg", (1920, 1080), "blue"),
    ("nature.png", (1200, 800), "green"),
    ("sunset.jpg", (1600, 1200), "orange"),
    ("flowers.png", (1000, 1000), "pink")
]

# STEP 4: Generate each image

for name, dimensions, color in image_details:

    image = Image.new(
        "RGB",
        dimensions,
        color
    )

    draw = ImageDraw.Draw(image)

    draw.text(
        (50, 50),
        name,
        fill="white"
    )

    image_path = input_folder / name

    image.save(image_path)

    print("Created:", name)

# STEP 5: Display the result

print("\nSample images created successfully!")

print("Input folder:", input_folder)

print("Output folder:", output_folder)
