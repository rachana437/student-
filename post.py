from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB config
app.config["MONGO_URI"] = "mongodb://localhost:27017/student_results"
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        mongo.db.students.insert_one({'name': name})
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    students = list(mongo.db.students.find())
    if request.method == 'POST':
        student_id = request.form['student_id']
        subject = request.form['subject']
        marks = int(request.form['marks'])
        mongo.db.results.insert_one({
            'student_id': ObjectId(student_id),
            'subject': subject,
            'marks': marks
        })
        return redirect(url_for('index'))
    return render_template('add_result.html', students=students)

@app.route('/results')
def view_results():
    results = mongo.db.results.aggregate([
        {
            '$lookup': {
                'from': 'students',
                'localField': 'student_id',
                'foreignField': '_id',
                'as': 'student_info'
            }
        }
    ])
    return render_template('view_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
