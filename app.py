from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib

# Non-GUI backend (Railway safe)
matplotlib.use("Agg")

app = Flask(__name__)

# Ensure static folder exists
os.makedirs("static", exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("files")

        dfs = {}
        for file in files:
            if file and file.filename.endswith(".csv"):
                dfs[file.filename] = pd.read_csv(file)

        # Required files
        students = dfs.get("students.csv")
        courses = dfs.get("courses.csv")
        enrollments = dfs.get("enrollments.csv")

        if students is None or courses is None or enrollments is None:
            return "Please upload students.csv, courses.csv, enrollments.csv"

        # Merge data
        df = enrollments.merge(students, on="Student_ID", how="left")
        df = df.merge(courses, on="Course_ID", how="left")

        # ===================== PLOTS =====================

        # Grade count
        plt.figure(figsize=(16, 6))
        ax = sns.countplot(x="Grade", data=df)
        for bars in ax.containers:
            ax.bar_label(bars)
        plt.title("Count of Students by Grade")
        plt.savefig("static/pass_fail.png")
        plt.close()

        # Gender vs Grade
        plt.figure(figsize=(8, 5))
        ax = sns.countplot(x="Gender", data=df, hue="Grade")
        for bars in ax.containers:
            ax.bar_label(bars, fontsize=8)
        plt.title("Students by Gender")
        plt.savefig("static/gender.png")
        plt.close()

        # Course wise
        plt.figure(figsize=(20, 7))
        ax = sns.countplot(x="Course_Name", data=df, hue="Grade")
        plt.xticks(rotation=45, ha="right")
        plt.title("Students by Course")
        plt.savefig("static/course.png")
        plt.close()

        # Binning
        df["Attendance_bin"] = pd.cut(df["Attendance"], bins=5)
        df["Study_Hours_bin"] = pd.cut(df["Study_Hours"], bins=5)
        df["Current_GPA_bin"] = pd.cut(df["Current_GPA"], bins=5)

        plt.figure(figsize=(10, 5))
        ax = sns.countplot(x="Department_y", data=df, hue="Grade")
        for bars in ax.containers:
            ax.bar_label(bars, fontsize=7)
        plt.title("Department vs Grade")
        plt.savefig("static/department.png")
        plt.close()

        return render_template(
            "result.html",
            tables=[df.head(5).to_html(classes="data", index=False)],
            graphs=[
                {"path": "static/pass_fail.png", "info": "Grade Distribution"},
                {"path": "static/gender.png", "info": "Gender Distribution"},
                {"path": "static/course.png", "info": "Course Distribution"},
                {"path": "static/department.png", "info": "Department Distribution"},
            ],
        )

    return render_template("upload.html")

