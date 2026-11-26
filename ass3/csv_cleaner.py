
import pandas as pd

# Step 1: Read the CSV file
df = pd.read_csv("customers.csv")

# Store the original number of records
total_records = len(df)

# Step 2: Remove unnecessary spaces
for column in df.columns:
    if df[column].dtype == "object":
        df[column] = df[column].str.strip()

# Convert empty values into missing values
df = df.replace("", pd.NA)

# Step 3: Remove duplicate records
before = len(df)

df = df.drop_duplicates()

duplicates_removed = before - len(df)

# Step 4: Standardise city names
df["City"] = df["City"].str.title()

# Step 5: Create a list to store invalid records
invalid_records = []

# Create a list to store valid records
valid_records = []

# Step 6: Check each row
for index, row in df.iterrows():

    errors = []

    # Check mandatory fields
    if pd.isna(row["Name"]):
        errors.append("Name is missing")

    if pd.isna(row["Email"]):
        errors.append("Email is missing")

    if pd.isna(row["City"]):
        errors.append("City is missing")

    # Check email format
    if pd.notna(row["Email"]):

        if "@" not in row["Email"] or "." not in row["Email"].split("@")[-1]:
            errors.append("Invalid email")

    # Step 7: Separate valid and invalid records
    if len(errors) > 0:

        row_data = row.to_dict()

        row_data["Reason"] = ", ".join(errors)

        invalid_records.append(row_data)

    else:
        valid_records.append(row.to_dict())


# Step 8: Convert lists into DataFrames
cleaned_df = pd.DataFrame(valid_records)

invalid_df = pd.DataFrame(invalid_records)

# Step 9: Save the output CSV files
cleaned_df.to_csv("cleaned_customers.csv", index=False)

invalid_df.to_csv("invalid_records.csv", index=False)

# Step 10: Display summary
print("DATA CLEANING SUMMARY")

print("----------------------")

print("Total records processed:", total_records)

print("Duplicates removed:", duplicates_removed)

print("Valid records:", len(cleaned_df))

print("Invalid records:", len(invalid_df))

print("\nCleaning completed successfully!")
