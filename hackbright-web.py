from flask import Flask, request, render_template
import hackbright


app = Flask(__name__)
#connect_to_db(app)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    rows = hackbright.get_grades_by_github(github)
    return render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           rows=rows)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def display_student_add_form():
    """Display form to add a student"""

    return render_template("student-add.html")


@app.route("/add-confirmation", methods=['POST'])
def student_add():
    """Add a student."""

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    github = request.form.get('github')

    QUERY = """
        INSERT INTO students
            VALUES (:firstname, :lastname, :github)
        """

    hackbright.db.session.execute(QUERY, {'firstname': firstname,
                               'lastname': lastname,
                               'github': github})
    hackbright.db.session.commit()

    return render_template("confirmation.html",
                           firstname=firstname,
                           lastname=lastname,
                           github=github)

@app.route("/project/<project_title>")
def display_project_info(project_title):

    title, description, max_grade = hackbright.get_project_by_title(project_title)

    # Outputs a list of tuples with (github, grade)
    github_grades = hackbright.get_grades_by_title(project_title)

    # List to hold tuples with (first, last, grade)
    student_grades = []

    for student in github_grades:
        # student[0] contains the github
        first, last, github = hackbright.get_student_by_github(student[0])
        # student[1] contains the students grades
        student_grades.append((first, last, student[1]))

    return render_template("project_info.html",
                           title=title,
                           description=description,
                           max_grade=max_grade,
                           student_grades=student_grades)


if __name__ == "__main__":
    #app = Flask(__name__)
    hackbright.connect_to_db(app)
    app.run(debug=True)
    hackbright.db.session.close()
