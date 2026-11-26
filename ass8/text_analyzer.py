
from pathlib import Path
from collections import Counter
import csv
import re


# STEP 1: Set the folder location

base_folder = Path(r"C:\Python_Automation\ass8")

input_folder = base_folder / "input_texts"

output_file = base_folder / "text_analysis_report.csv"


# STEP 2: Define common words to ignore

common_words = {
    "the", "is", "and", "a", "an",
    "to", "of", "in", "it", "i",
    "was", "are", "for", "with",
    "this", "that", "very", "also",
    "because", "my", "am", "be"
}


# STEP 3: Find all text files

text_files = list(input_folder.glob("*.txt"))


# STEP 4: Create variables to store results

report_data = []

overall_word_count = Counter()

total_words = 0

total_lines = 0

total_characters = 0


# STEP 5: Read and analyse each text file

for file_path in text_files:

    try:

        # Read the text file
        content = file_path.read_text(
            encoding="utf-8"
        )

        # STEP 6: Calculate total characters

        character_count = len(content)

        # STEP 7: Calculate total lines

        line_count = len(content.splitlines())

        # STEP 8: Identify all words

        words = re.findall(
            r"\b[a-zA-Z']+\b",
            content.lower()
        )

        # Count all words
        word_count = len(words)

        # STEP 9: Remove common words

        filtered_words = []

        for word in words:

            if word not in common_words:

                filtered_words.append(word)

        # STEP 10: Count word frequency

        word_frequency = Counter(filtered_words)

        # Find the five most frequent words
        most_common_words = word_frequency.most_common(5)

        # Convert word counts into readable text
        frequent_words_text = ", ".join(
            [
                word + " (" + str(count) + ")"
                for word, count in most_common_words
            ]
        )

        # STEP 11: Add file word counts to overall count

        overall_word_count.update(filtered_words)

        # Add statistics to totals
        total_words += word_count

        total_lines += line_count

        total_characters += character_count

        # STEP 12: Store file information

        report_data.append([
            file_path.name,
            word_count,
            line_count,
            character_count,
            frequent_words_text
        ])

        # STEP 13: Display file results

        print("\nFile:", file_path.name)

        print("Total Words:", word_count)

        print("Total Lines:", line_count)

        print("Total Characters:", character_count)

        print("Most Frequent Words:", frequent_words_text)

    except Exception as error:

        print("\nCould not process:", file_path.name)

        print("Reason:", error)


# STEP 14: Find most frequent words across all files

overall_most_common = overall_word_count.most_common(5)

overall_frequent_text = ", ".join(
    [
        word + " (" + str(count) + ")"
        for word, count in overall_most_common
    ]
)


# STEP 15: Generate CSV report

with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as csv_file:

    writer = csv.writer(csv_file)

    # Write column headings

    writer.writerow([
        "File Name",
        "Total Words",
        "Total Lines",
        "Total Characters",
        "Most Frequent Words"
    ])

    # Write individual file details

    writer.writerows(report_data)

    # Write overall summary

    writer.writerow([
        "OVERALL SUMMARY",
        total_words,
        total_lines,
        total_characters,
        overall_frequent_text
    ])


# STEP 16: Display final summary

print("\n---------- FINAL SUMMARY ----------")

print("Total Files Analysed:", len(report_data))

print("Total Words:", total_words)

print("Total Lines:", total_lines)

print("Total Characters:", total_characters)

print("\nMost Frequent Words Across All Files:")

print(overall_frequent_text)

print("\nReport saved at:", output_file)

print("\nText analysis completed successfully!")
