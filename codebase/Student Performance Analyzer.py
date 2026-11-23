import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

CSV_FILE = "students.csv"

def get_grade(percentage):
    if percentage >= 90:
        return "A"
    elif percentage >= 75:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

def load_data():
    if not os.path.exists(CSV_FILE):
        print("students.csv file not found!")
        return None

    # Read without header - file is like: Aman,80,70,90
    try:
        df = pd.read_csv(CSV_FILE, header=None, names=["Name", "Maths", "Physics", "Chemistry"])
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

    valid_rows = []
    for index, row in df.iterrows():
        name = row["Name"]
        try:
            maths = float(row["Maths"])
            physics = float(row["Physics"])
            chemistry = float(row["Chemistry"])
        except ValueError:
            # Find which subject is invalid
            for subject in ["Maths", "Physics", "Chemistry"]:
                try:
                    float(row[subject])
                except:
                    print(f"Invalid marks for {name} in {subject}: '{row[subject]}'. Row skipped.")
                    break
            continue

        # Check marks 0 to 100
        if not (0 <= maths <= 100 and 0 <= physics <= 100 and 0 <= chemistry <= 100):
            print(f"Invalid marks for {name}. Marks must be 0-100. Row skipped.")
            continue

        total = maths + physics + chemistry
        percentage = total / 300 * 100
        grade = get_grade(percentage)
        valid_rows.append([name, maths, physics, chemistry, total, percentage, grade])

    if not valid_rows:
        print("No valid data found.")
        return None

    result_df = pd.DataFrame(valid_rows, columns=["Name", "Maths", "Physics", "Chemistry", "Total", "Percentage", "Grade"])
    return result_df

# Option 1: Result
def show_result():
    df = load_data()
    if df is None:
        return
    print("\n--- Student Result ---")
    for _, row in df.iterrows():
        print(f"{row['Name']} | {int(row['Total'])} | {row['Percentage']:.2f}% | {row['Grade']}")

# Option 2: Statistics + Charts
def show_statistics():
    df = load_data()
    if df is None:
        return

    percentages = df["Percentage"].values
    mean_val = np.mean(percentages)
    median_val = np.median(percentages)
    std_val = np.std(percentages)

    print(f"\nMean %: {mean_val:.2f} | Median %: {median_val:.2f} | Std Dev: {std_val:.2f}")

    # Topper
    topper_row = df.loc[df["Percentage"].idxmax()]
    print(f"Topper: {topper_row['Name']} ({topper_row['Percentage']:.2f}%)")

    # Subject averages using Pandas
    maths_avg = df["Maths"].mean()
    physics_avg = df["Physics"].mean()
    chemistry_avg = df["Chemistry"].mean()
    print(f"Subject averages: Maths {maths_avg:.2f}, Physics {physics_avg:.2f}, Chemistry {chemistry_avg:.2f}")

    # Bar Chart - Total Marks
    plt.figure(figsize=(8, 5))
    plt.bar(df["Name"], df["Total"], color="skyblue")
    plt.title("Student Total Marks")
    plt.xlabel("Student Name")
    plt.ylabel("Total Marks (out of 300)")
    plt.ylim(0, 300)
    plt.show()

    # Histogram - Percentage Distribution
    plt.figure(figsize=(8, 5))
    plt.hist(df["Percentage"], bins=5, color="lightgreen", edgecolor="black")
    plt.title("Percentage Distribution")
    plt.xlabel("Percentage (%)")
    plt.ylabel("Number of Students")
    plt.show()

    print("Bar chart displayed")

# Main Menu
def main():
    while True:
        print("\n--- Student Performance Analyzer ---")
        print("1. Result")
        print("2. Statistics")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            show_result()
        elif choice == "2":
            show_statistics()
        elif choice == "3":
            print("Thank you! Goodbye.")
            break
        else:
            print("Invalid choice! Try again.")

main()
