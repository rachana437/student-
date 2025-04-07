from flask import Flask, render_template, request, redirect, url_for
from models import db, Student, Result

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        new_student = Student(name=name)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    students = Student.query.all()
    if request.method == 'POST':
        student_id = request.form['student_id']
        subject = request.form['subject']
        marks = request.form['marks']
        result = Result(student_id=student_id, subject=subject, marks=marks)
        db.session.add(result)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_result.html', students=students)

@app.route('/results')
def view_results():
    results = Result.query.join(Student).add_columns(Student.name, Result.subject, Result.marks)
    return render_template('view_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
