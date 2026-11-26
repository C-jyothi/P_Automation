
import pandas as pd
import os
import glob

# Step 1: Give the sales folder path
# folder_path = r"C:\Users\YourName\Desktop\Assignment_4\sales"
folder_path = r"C:\Python_Automation\ass4\sales"

# Step 2: Find all Excel files in the folder
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

# Step 3: Check whether Excel files are available
if len(excel_files) == 0:

    print("No Excel files found in the folder.")

else:

    all_data = []
    invalid_count = 0

    # Step 4: Read each Excel file
    for file in excel_files:

        try:

            df = pd.read_excel(file)

            # Required columns
            required_columns = [
                "Date",
                "Product",
                "Category",
                "Quantity",
                "Unit Price"
            ]

            # Check whether required columns exist
            if not all(column in df.columns for column in required_columns):

                print("Required columns missing in:", file)
                continue

            # Step 5: Clean the data
            df["Product"] = df["Product"].astype("string").str.strip()

            df["Category"] = df["Category"].astype("string").str.strip()

            df["Date"] = pd.to_datetime(
                df["Date"],
                errors="coerce",
                dayfirst=True
            )

            df["Quantity"] = pd.to_numeric(
                df["Quantity"],
                errors="coerce"
            )

            df["Unit Price"] = pd.to_numeric(
                df["Unit Price"],
                errors="coerce"
            )

            # Count records before cleaning
            before = len(df)

            # Remove rows containing missing or incorrect values
            df = df.dropna(
                subset=[
                    "Date",
                    "Product",
                    "Category",
                    "Quantity",
                    "Unit Price"
                ]
            )

            # Count invalid records removed
            invalid_count = invalid_count + (before - len(df))

            # Store cleaned data
            all_data.append(df)

        except Exception as e:

            print("Could not read file:", file)
            print("Reason:", e)

    # Step 6: Combine all Excel files
    if len(all_data) == 0:

        print("No valid Excel data available.")

    else:

        combined_df = pd.concat(all_data, ignore_index=True)

        # Step 7: Calculate total sales
        combined_df["Total Sales"] = (
            combined_df["Quantity"] * combined_df["Unit Price"]
        )

        # Step 8: Product-wise summary
        product_summary = combined_df.groupby("Product").agg(
            Total_Quantity=("Quantity", "sum"),
            Total_Revenue=("Total Sales", "sum")
        ).reset_index()

        # Sort products by quantity sold
        product_summary = product_summary.sort_values(
            by="Total_Quantity",
            ascending=False
        )

        # Step 9: Category-wise summary
        category_summary = combined_df.groupby("Category").agg(
            Total_Quantity=("Quantity", "sum"),
            Total_Revenue=("Total Sales", "sum")
        ).reset_index()

        # Step 10: Overall summary
        total_revenue = combined_df["Total Sales"].sum()

        total_quantity = combined_df["Quantity"].sum()

        total_transactions = len(combined_df)

        best_selling_product = product_summary.iloc[0]["Product"]

        overall_summary = pd.DataFrame({
            "Description": [
                "Total Revenue",
                "Total Quantity Sold",
                "Total Transactions",
                "Best Selling Product",
                "Invalid Records Removed"
            ],

            "Value": [
                total_revenue,
                total_quantity,
                total_transactions,
                best_selling_product,
                invalid_count
            ]
        })

        # Step 11: Create the Excel report
        output_file = os.path.join(
            folder_path,
            "consolidated_report.xlsx"
        )

        with pd.ExcelWriter(
            output_file,
            engine="openpyxl"
        ) as writer:

            combined_df.to_excel(
                writer,
                sheet_name="All Transactions",
                index=False
            )

            product_summary.to_excel(
                writer,
                sheet_name="Product Summary",
                index=False
            )

            category_summary.to_excel(
                writer,
                sheet_name="Category Summary",
                index=False
            )

            overall_summary.to_excel(
                writer,
                sheet_name="Overall Summary",
                index=False
            )

        # Step 12: Display the result
        print("\nExcel Report Created Successfully!")

        print("Total Transactions:", total_transactions)

        print("Total Quantity Sold:", total_quantity)

        print("Total Revenue:", total_revenue)

        print("Best Selling Product:", best_selling_product)

        print("Invalid Records Removed:", invalid_count)

        print("Report saved at:", output_file)
