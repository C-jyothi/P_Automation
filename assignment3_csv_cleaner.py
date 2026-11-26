
from pathlib import Path
import pandas as pd
import re

# STEP 1: Get project folder
base_folder = Path(__file__).parent

# STEP 2: Customer data folder
customer_folder = base_folder / "CustomerData"

# Check whether CustomerData folder exists
if not customer_folder.exists():

    print("CustomerData folder does not exist!")

else:

    # STEP 3: Display available CSV files
    print("\nAvailable CSV files:")

    csv_files = list(customer_folder.glob("*.csv"))

    for file in csv_files:
        print("-", file.name)

    # STEP 4: Ask which file to clean
    file_name = input(
        "\nEnter the CSV filename you want to clean: "
    ).strip().strip('"')

    file_path = customer_folder / file_name

    # STEP 5: Check whether file exists
    if not file_path.exists() or not file_path.is_file():

        print("Error: CSV file not found!")

    elif file_path.suffix.lower() != ".csv":

        print("Please select a CSV file.")

    else:

        try:

            # STEP 6: Read CSV file
            df = pd.read_csv(
                file_path,
                dtype=str,
                keep_default_na=False
            )

            required_columns = [
                "Name", "Email", "Phone", "City"
            ]

            # STEP 7: Check required columns
            if not all(column in df.columns for column in required_columns):

                print("CSV must contain Name, Email, Phone and City columns.")

            else:

                total_records = len(df)

                # STEP 8: Remove unnecessary spaces
                for column in required_columns:

                    df[column] = df[column].str.strip()

                # STEP 9: Standardise city names
                df["City"] = df["City"].str.title()

                # STEP 10: Remove duplicate records
                before_duplicates = len(df)

                df = df.drop_duplicates()

                duplicates_removed = before_duplicates - len(df)

                # STEP 11: Create valid and invalid lists
                valid_records = []

                invalid_records = []

                # STEP 12: Check each customer record
                for _, row in df.iterrows():

                    errors = []

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

                    record = row.to_dict()

                    # STEP 13: Separate valid and invalid records
                    if errors:

                        record["Reason"] = ", ".join(errors)

                        invalid_records.append(record)

                    else:

                        valid_records.append(record)

                # STEP 14: Create Output folder
                output_folder = base_folder / "Output"

                output_folder.mkdir(exist_ok=True)

                # STEP 15: Save cleaned records
                cleaned_df = pd.DataFrame(
                    valid_records,
                    columns=required_columns
                )

                cleaned_df.to_csv(
                    output_folder / "cleaned_customers.csv",
                    index=False
                )

                # STEP 16: Save invalid records
                invalid_df = pd.DataFrame(
                    invalid_records,
                    columns=required_columns + ["Reason"]
                )

                invalid_df.to_csv(
                    output_folder / "invalid_records.csv",
                    index=False
                )

                # STEP 17: Display summary
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
