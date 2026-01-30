from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import matplotlib
matplotlib.use('Agg') 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        files = request.files.getlist("files")

        # Dictionary বানাই যাতে ফাইল নাম দিয়ে আলাদা DataFrame রাখা যায়
        dfs = {}
        for file in files:
            if file.filename.endswith(".csv"):
                df = pd.read_csv(file)
                dfs[file.filename] = df

        # ধরো ফাইল নাম students.csv, courses.csv, enrollments.csv
        students = dfs.get("students.csv")
        courses = dfs.get("courses.csv")
        enrollments = dfs.get("enrollments.csv")

        # Merge করা
        df = enrollments.merge(students, on="Student_ID", how="left")
        df = df.merge(courses, on="Course_ID", how="left")

        # count Gread 
        # count Gread 
        plt.rcParams['figure.figsize'] = (16,6)
        ax = sns.countplot(x = df['Grade'],data = df,hue='Grade')
        for bars in ax.containers:
            ax.bar_label(bars)
        plt.title("Count of Student By Gread",fontsize = 25)
        plt.savefig("static/pass_fail.png")

        plt.figure(figsize=(8,5))
        ax = sns.countplot(x = df['Gender'],data = df,hue="Grade",palette="Set1")
        for bars in ax.containers:
            ax.bar_label(bars, fontsize=8, padding=3)
        plt.title("Students by Gender")
        plt.savefig("static/gender.png")

        # Countplot for Course_Name
        plt.figure(figsize=(25,8))
        ax = sns.countplot(x = df['Course_Name'],data = df,hue="Grade",palette="Set1")
        for bars in ax.containers:
            ax.bar_label(bars,fontsize=20,padding=5,rotation=90,)
        plt.title("Students by Course_Name",fontsize = 20)
        plt.legend(title="Grade",fontsize=20,title_fontsize=20,loc='upper right',bbox_to_anchor=(1.15, 1)) # Adjust legend position
        plt.savefig("static/Course_Name.png")


        # Binning continuous variables
        df["Attendance_bin"] = pd.cut(df["Attendance"], bins=5)
        df["Study_Hours_bin"] = pd.cut(df["Study_Hours"], bins=5)
        df["Current_GPA_bin"] = pd.cut(df["Current_GPA"], bins=5)

        # Columns to plot
        columns = [
            "Year",
            "Attendance_bin",
            "Study_Hours_bin",
            "Current_GPA_bin",
            "Course_Name"
        ]

        hue_col = "Department_x"

        # Create subplots
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        axes = axes.flatten()

        # Plot countplots with hue
        for ax, col in zip(axes, columns):
            sns.countplot(
                data=df,
                x=col,
                hue=hue_col,
                order=df[col].value_counts().index,
                ax=ax
            )
            ax.set_title(f"{col} by {hue_col}")
            ax.tick_params(axis='x', rotation=45)

        # Remove unused axes
        for i in range(len(columns), len(axes)):
            fig.delaxes(axes[i])

        # Move legend outside
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, title=hue_col, loc="upper right")

        # Remove individual legends
        for ax in axes[:len(columns)]:
            ax.get_legend().remove()

        plt.tight_layout(rect=[0, 0, 0.9, 1])
        plt.savefig("static/Bind.png")

        plt.figure(figsize=(10,5))
        ax = sns.countplot(x = df['Department_y'],data = df,hue="Grade",palette="Set1")
        for bars in ax.containers:
            ax.bar_label(bars, fontsize=8, padding=5)
        plt.title("Students by Department and Grade")
        plt.legend(title="Grade",fontsize=10,title_fontsize=10,loc='upper right',bbox_to_anchor=(1.15, 1)) # Adjust legend position
        plt.savefig("static/dpandgrad.png")

        # years = range(2000, 2025)
        # passrate = [9,9.11,9.99,11,13,10,14,15,18,15,20,21.23,22.89,29.2,30,35,35.33,40,44,45,45.89,50,51.34,53,55]
        # plt.plot(years, passrate)
    

        # plt.xlabel('Year')
        # plt.ylabel('Pass rate')

        # plt.title("Student pass Rate")
        # plt.savefig("static/studentpassrate.png")

        return render_template("result.html",
                               tables=[df.head(5).to_html(classes='data')],
                                graphs=[ {"path": "static/pass_fail.png", "info": "Pass vs Fail distribution"}, 
                                        {"path": "static/gender.png", "info": "Gender ratio of students"}, 
                                        {"path": "static/Course_Name.png", "info": "Course ratio of students"}, 
                                        {"path": "static/Bind.png", "info": "Course ratio of students"}, 
                                        {"path": "static/dpandgrad.png", "info": "Course ratio of students"},] )

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
