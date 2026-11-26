
from pathlib import Path
import pandas as pd
import re

# Project folder
base_folder = Path(__file__).parent

# Ask the user for the CSV file
file_name = input("Enter CSV file path or name: ").strip().strip('"')

# If only a filename is entered, look inside CustomerData
file_path = Path(file_name)

if not file_path.is_absolute():
    if not file_path.exists():
        file_path = base_folder / "CustomerData" / file_name

# Check whether the file exists
if not file_path.exists():
    print("Error: CSV file not found.")

else:
    try:
        # Read CSV file
        df = pd.read_csv(file_path, dtype=str, keep_default_na=False)

        # Check required columns
        required_columns = ["Name", "Email", "Phone", "City"]

        if not all(column in df.columns for column in required_columns):
            print("Error: CSV must contain Name, Email, Phone and City columns.")

        else:
            total_records = len(df)

            # Remove unnecessary spaces from text columns
            for column in required_columns:
                df[column] = df[column].str.strip()

            # Standardise city names
            df["City"] = df["City"].str.title()

            # Remove duplicate records
            before_duplicates = len(df)
            df = df.drop_duplicates()
            duplicates_removed = before_duplicates - len(df)

            # Store valid and invalid records
            valid_records = []
            invalid_records = []

            # Check each row
            for _, row in df.iterrows():

                errors = []

                # Check mandatory fields
                if not row["Name"]:
                    errors.append("Missing Name")

                if not row["Email"]:
                    errors.append("Missing Email")
                elif not re.match(
                    r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                    row["Email"]
                ):
                    errors.append("Invalid Email Format")

                if not row["Phone"]:
                    errors.append("Missing Phone")

                # Separate valid and invalid records
                record = row.to_dict()

                if errors:
                    record["Reason"] = ", ".join(errors)
                    invalid_records.append(record)
                else:
                    valid_records.append(record)

            # Create output folder
            output_folder = base_folder / "Output"
            output_folder.mkdir(exist_ok=True)

            # Save cleaned CSV
            cleaned_df = pd.DataFrame(
                valid_records,
                columns=required_columns
            )

            cleaned_df.to_csv(
                output_folder / "cleaned_customers.csv",
                index=False
            )

            # Save invalid CSV
            invalid_df = pd.DataFrame(
                invalid_records,
                columns=required_columns + ["Reason"]
            )

            invalid_df.to_csv(
                output_folder / "invalid_records.csv",
                index=False
            )

            # Display summary
            print("\n========== CLEANING SUMMARY ==========")
            print("Total records processed:", total_records)
            print("Duplicates removed:", duplicates_removed)
            print("Valid records:", len(valid_records))
            print("Invalid records:", len(invalid_records))
            print("======================================")

            print("\nFiles created successfully!")
            print("Output folder:", output_folder)

    except Exception as error:
        print("An error occurred:", error)
