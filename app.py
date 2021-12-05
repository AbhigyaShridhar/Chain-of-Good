from flask import Flask, render_template, json, current_app, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

#initialiing flask app
app = Flask(__name__)

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

#model for storing JSON objects
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    domain = db.Column(db.String)
    contact = db.Column(db.String)
    location = db.Column(db.String)
    age = db.Column(db.Integer)
    picture = db.Column(db.String)

    def __repr__(self):
        return '<Student %r>' % self.name

    #student = Student(name, contact, domain, location, age, picture)
    def __init__(self, name, contact, domain, location, age, picture):
        self.name = name
        self.contact = contact
        self.domain = domain
        self.location = location
        self.age = age
        self.picture = picture

#initialize relation
db.create_all()

#API configuration
from marshmallow_jsonapi.flask import Schema
from marshmallow_jsonapi import fields

class StudentSchema(Schema):
    class Meta:
        type_ = 'student'
        self_view = 'student_one'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'student_all'

    id = fields.Integer()
    name = fields.Str(required=True)
    contact = fields.Str(load_only=True)
    domain = fields.Str()
    location = fields.Str()
    age = fields.Integer()
    picture = fields.Url()

#api routes
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList

class StudentMany(ResourceList):
    schema = StudentSchema
    data_layer = {
        'session': db.session,
        'model': Student
    }

class StudentOne(ResourceDetail):
    schema = StudentSchema
    data_layer = {
        'session': db.session,
        'model': Student
    }

api = Api(app)
api.route(StudentMany, 'student_all', '/data/students')
api.route(StudentOne, 'student_one', '/students/<int:id>')

#app routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contract/adoption')
def get_contract_data():
    filename = os.path.join(current_app.static_folder, 'data', 'Adoption.json')
    with open(filename) as test_file:
        data = json.load(test_file)
    return jsonify(data)

@app.route('/students/add', methods=['POST'])
def isert_data():
    name = request.form["name"]
    domain = request.form["domain"]
    contact = request.form["contact"]
    location = request.form["location"]
    picture = request.form["picture"]
    age = request.form["age"]
    student = Student(name, contact, domain, location, age, picture)
    db.session.add(student)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
