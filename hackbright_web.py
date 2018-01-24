"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    performance = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           performance=performance)
    return html
    # return "{acct} is the GitHub account for {first} {last}".format(
    #     acct=github, first=first, last=last)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student"""

    return render_template("student_search.html")


@app.route("/student-add")
def student_add():
    """Add a student."""

    return render_template("add_student.html")


@app.route("/new-student", methods=['POST'])
def new_student():
    """Show the new student added"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    github = request.form.get("github")

    hackbright.make_new_student(fname, lname, github)

    return render_template("student_added.html",
                           github=github)

@app.route("/project")
def project_info():
    """Will show title, description, max grade of a project"""
    student_name =[]

    project = request.args.get('project')

    title, description, max_grade = hackbright.get_project_by_title(project)
    github_grades = hackbright.get_grades_by_title(project)

    for github, grades in github_grades:
        first_name, last_name = hackbright.get_student_by_github(github)
        student_name.append(first_name, last_name, grade)  ####

    html_project = render_template("find_project.html",
                                   title=title,
                                   description=description,
                                   max_grade=max_grade,
                                   names=student_name)

    return html_project

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
