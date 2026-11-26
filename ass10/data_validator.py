
import pandas as pd
import json
import re

from pathlib import Path


# STEP 1: Set folder locations

base_folder = Path(r"C:\Python_Automation\ass10")

input_folder = base_folder / "input_files"

output_folder = base_folder / "output_files"


# STEP 2: Select the input file

# You can select either CSV or Excel

input_file = input_folder / "employees.csv"

# For Excel, use this instead:
# input_file = input_folder / "employees.xlsx"


# STEP 3: Set the validation rules file

rules_file = base_folder / "validation_rules.json"


# STEP 4: Create the output folder

output_folder.mkdir(parents=True, exist_ok=True)


# STEP 5: Read the input file

def read_input_file(file_path):

    extension = file_path.suffix.lower()

    if extension == ".csv":

        return pd.read_csv(file_path)

    elif extension in [".xlsx", ".xls"]:

        return pd.read_excel(file_path)

    else:

        raise ValueError("Only CSV and Excel files are supported.")


# STEP 6: Read the JSON validation rules

def load_validation_rules(file_path):

    with open(file_path, "r", encoding="utf-8") as file:

        rules = json.load(file)

    return rules


# STEP 7: Check whether a value is empty

def is_empty(value):

    if pd.isna(value):

        return True

    if isinstance(value, str) and value.strip() == "":

        return True

    return False


# STEP 8: Validate email addresses

def validate_email(value):

    pattern = r"^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$"

    return bool(re.match(pattern, str(value)))


# STEP 9: Validate phone numbers

def validate_phone(value):

    phone = str(value).strip()

    pattern = r"^\d{10}$"

    return bool(re.fullmatch(pattern, phone))


# STEP 10: Validate numeric values

def validate_integer(value):

    try:

        number = float(value)

        return number.is_integer()

    except (ValueError, TypeError):

        return False


# STEP 11: Validate each employee record

def validate_record(row, rules):

    errors = []

    for column, rule in rules.items():

        value = row.get(column)

        # Check mandatory fields

        if rule.get("required", False) and is_empty(value):

            errors.append(column + " is missing")

            continue

        # Skip other checks for empty optional fields

        if is_empty(value):

            continue

        # Check email format

        if rule.get("type") == "email":

            if not validate_email(value):

                errors.append(column + " has an invalid email format")

        # Check phone number

        if rule.get("type") == "phone":

            if not validate_phone(value):

                errors.append(column + " must contain 10 digits")

        # Check integer values and numeric range

        if rule.get("type") == "integer":

            if not validate_integer(value):

                errors.append(column + " must be an integer")

            else:

                number = float(value)

                if "min" in rule and number < rule["min"]:

                    errors.append(
                        column + " must be at least " + str(rule["min"])
                    )

                if "max" in rule and number > rule["max"]:

                    errors.append(
                        column + " must not exceed " + str(rule["max"])
                    )

        # Check allowed values

        if "allowed_values" in rule:

            allowed = rule["allowed_values"]

            if str(value).strip() not in allowed:

                errors.append(
                    column + " contains an unallowed value"
                )

    return errors


# STEP 12: Main validation process

def process_data():

    try:

        # Read employee data

        df = read_input_file(input_file)

        # Load validation rules

        rules = load_validation_rules(rules_file)

        # Check whether required columns exist

        missing_columns = [
            column for column in rules
            if column not in df.columns
        ]

        if missing_columns:

            raise ValueError(
                "Missing columns: " + ", ".join(missing_columns)
            )

        # Store valid and invalid records

        valid_records = []

        invalid_records = []

        # Find duplicate records

        duplicate_rows = df.duplicated(keep="first")

        # Check each row

        for index, row in df.iterrows():

            # Validate the employee information

            errors = validate_record(row, rules)

            # Check duplicate records

            if duplicate_rows.iloc[index]:

                errors.append("Duplicate record")

            # Convert row into a dictionary

            record = row.to_dict()

            # Store invalid records with error descriptions

            if errors:

                record["Errors"] = "; ".join(errors)

                invalid_records.append(record)

            else:

                valid_records.append(record)

        # Convert results into DataFrames

        valid_df = pd.DataFrame(valid_records)

        invalid_df = pd.DataFrame(invalid_records)

        # STEP 13: Save valid records

        valid_file = output_folder / "valid_records.csv"

        valid_df.to_csv(valid_file, index=False)

        # STEP 14: Save invalid records

        invalid_file = output_folder / "invalid_records.csv"

        invalid_df.to_csv(invalid_file, index=False)

        # STEP 15: Display summary

        total_records = len(df)

        valid_count = len(valid_records)

        invalid_count = len(invalid_records)

        print("\n---------- VALIDATION SUMMARY ----------")

        print("Total Records Processed:", total_records)

        print("Valid Records:", valid_count)

        print("Invalid Records:", invalid_count)

        print("\nValid records saved at:")

        print(valid_file)

        print("\nInvalid records saved at:")

        print(invalid_file)

        print("\nData validation completed successfully!")

    except FileNotFoundError as error:

        print("File not found:", error)

    except PermissionError:

        print("Permission denied. Close the output files and try again.")

    except Exception as error:

        print("An error occurred:", error)


# STEP 16: Run the program

process_data()
