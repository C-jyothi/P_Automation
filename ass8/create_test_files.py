
from pathlib import Path

# STEP 1: Set the main folder location

base_folder = Path(r"C:\Python_Automation\ass8")

# STEP 2: Create the input folder

input_folder = base_folder / "input_texts"

input_folder.mkdir(parents=True, exist_ok=True)

# STEP 3: Create sample feedback contents

feedback1 = """The product is very good.

The product quality is excellent.

I like the product because it is useful.

The customer service is also good.
"""

feedback2 = """The delivery was fast and the product was excellent.

The product quality is very good.

I am happy with the product.

The delivery service was good.
"""

feedback3 = """The product is affordable and useful.

I like the quality of the product.

The customer service was helpful.

The product is excellent.
"""

# STEP 4: Store file names and contents

sample_files = {
    "feedback1.txt": feedback1,
    "feedback2.txt": feedback2,
    "feedback3.txt": feedback3
}

# STEP 5: Create the text files

for file_name, content in sample_files.items():

    file_path = input_folder / file_name

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    print("Created:", file_name)

# STEP 6: Display the result

print("\nSample text files created successfully!")

print("\nInput folder:", input_folder)

print("\nFiles created:")

for file_path in input_folder.iterdir():

    if file_path.is_file():

        print(file_path.name)

print("\nYou can now run text_analyzer.py!")
