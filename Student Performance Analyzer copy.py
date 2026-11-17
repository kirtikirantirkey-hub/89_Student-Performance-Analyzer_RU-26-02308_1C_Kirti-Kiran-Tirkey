import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Grade Function - FIXED Line 8,10,12,14
def calculate_grade(percentage):
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

# 2. Load Data - FIXED File Name to students.csv
def load_data():
    try:
        # Check if file has header or not
        with open("students.csv", "r") as f:
            first_line = f.readline()
        has_header = "Name" in first_line

        if has_header:
            df = pd.read_csv("students.csv", dtype=str, keep_default_na=False)
        else:
            df = pd.read_csv("students.csv", header=None, names=["Name", "Maths", "Physics", "Chemistry"], dtype=str, keep_default_na=False)

        subjects = ["Maths", "Physics", "Chemistry"]
        valid_rows = []

        for index, row in df.iterrows():
            name = row["Name"]
            is_valid = True
            marks = {}
            for subject in subjects:
                val_str = str(row[subject]).strip()
                try:
                    val = float(val_str)
                    if val < 0 or val > 100:
                        raise ValueError
                    marks[subject] = val
                except:
                    # FIXED Invalid Message
                    print(f"Invalid marks for {name} in {subject}: '{val_str}'. Row skipped.")
                    is_valid = False
                    break
            if is_valid:
                valid_rows.append({"Name": name, "Maths": marks["Maths"], "Physics": marks["Physics"], "Chemistry": marks["Chemistry"]})

        return pd.DataFrame(valid_rows)

    except FileNotFoundError:
        print("students.csv file not found!")
        return pd.DataFrame()

# 3. Show Result
def show_result(df):
    if df.empty:
        print("No valid student records found.")
        return

    df = df.copy()
    df["Total"] = df[["Maths", "Physics", "Chemistry"]].sum(axis=1)
    df["Percentage"] = df["Total"] / 3
    df["Grade"] = df["Percentage"].apply(calculate_grade)

    print("\n--- STUDENT RESULT ---")
    for index, row in df.iterrows():
        print(f"{row['Name']} | {int(row['Total'])} | {row['Percentage']:.2f}% | {row['Grade']}")

# 4. Show Statistics - FIXED Format to 1 Line
def show_statistics(df):
    if df.empty:
        print("No valid student records found.")
        return

    df = df.copy()
    df["Percentage"] = df[["Maths", "Physics", "Chemistry"]].sum(axis=1) / 3

    mean = np.mean(df["Percentage"])
    median = np.median(df["Percentage"])
    std = np.std(df["Percentage"])  # Gives 15.77

    print("\n--- CLASS STATISTICS ---")
    print(f"Mean %: {mean:.2f} | Median %: {median:.2f} | Std Dev: {std:.2f}")

    topper = df.loc[df["Percentage"].idxmax()]
    print(f"Topper: {topper['Name']} ({topper['Percentage']:.2f}%)")

    subjects = ["Maths", "Physics", "Chemistry"]
    print("Subject averages: ", end="")
    print(", ".join([f"{s} {df[s].mean():.2f}" for s in subjects]))

    # Bar Chart
    df[subjects].mean().plot(kind="bar")
    plt.title("Subject-wise Average Marks")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.show()

    # Histogram
    plt.hist(df["Percentage"], bins=5)
    plt.title("Student Percentage Distribution")
    plt.xlabel("Percentage")
    plt.ylabel("Number of Students")
    plt.show()

# 5. Main Program
def main():
    df = load_data()
    while True:
        print("\n--- STUDENT PERFORMANCE ANALYZER ---")
        print("1. Results")
        print("2. Statistics")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            show_result(df)
        elif choice == "2":
            show_statistics(df)
        elif choice == "3":
            print("Thank you!")
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()
    