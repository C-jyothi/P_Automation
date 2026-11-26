
from pathlib import Path
import pandas as pd
import json


# STEP 1: Create the main folder

base_folder = Path(r"C:\Python_Automation\ass10")


# STEP 2: Create input and output folders

input_folder = base_folder / "input_files"

output_folder = base_folder / "output_files"

input_folder.mkdir(parents=True, exist_ok=True)

output_folder.mkdir(parents=True, exist_ok=True)


# STEP 3: Create sample employee data

employee_data = {

    "Name": [
        "John",
        "Mary",
        "Alex",
        "David",
        "Priya",
        "Anu",
        "John"
    ],

    "Email": [
        "john@gmail.com",
        "marygmail.com",
        "alex@gmail.com",
        "",
        "priya@gmail.com",
        "anu@gmail.com",
        "john@gmail.com"
    ],

    "Phone": [
        "9876543210",
        "9876543211",
        "9876543212",
        "9876543213",
        "9876543214",
        "12345",
        "9876543210"
    ],

    "Age": [
        25,
        30,
        15,
        28,
        65,
        35,
        25
    ],

    "Department": [
        "IT",
        "HR",
        "Sales",
        "Finance",
        "Marketing",
        "IT",
        "IT"
    ]
}


# STEP 4: Convert the data into a DataFrame

df = pd.DataFrame(employee_data)


# STEP 5: Create a CSV file

csv_file = input_folder / "employees.csv"

df.to_csv(csv_file, index=False)


# STEP 6: Create an Excel file

excel_file = input_folder / "employees.xlsx"

df.to_excel(excel_file, index=False)


# STEP 7: Create validation rules

validation_rules = {

    "Name": {
        "required": True
    },

    "Email": {
        "required": True,
        "type": "email"
    },

    "Phone": {
        "required": True,
        "type": "phone"
    },

    "Age": {
        "required": True,
        "type": "integer",
        "min": 18,
        "max": 60
    },

    "Department": {
        "required": True,
        "allowed_values": [
            "HR",
            "IT",
            "Finance",
            "Sales"
        ]
    }
}


# STEP 8: Save rules as a JSON file

rules_file = base_folder / "validation_rules.json"

with open(rules_file, "w", encoding="utf-8") as file:

    json.dump(
        validation_rules,
        file,
        indent=4
    )


# STEP 9: Display the result

print("Sample files created successfully!")

print("\nCreated folders:")
print(input_folder)
print(output_folder)

print("\nCreated files:")
print(csv_file)
print(excel_file)
print(rules_file)

print("\nYou can now run data_validator.py!")
