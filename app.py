from flask import Flask, session, url_for, render_template, json, current_app, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

#initializing environment variables:
from decouple import config
AC_SID = config("AC_SID")
AUTH_TOKEN = config("AUTH_TOKEN")
VERIFY = config("VERIFY")

#initialiing flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sadfdsafdsaf786sf7sdaf7witb4i7th746htdr467it'

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

from twilio.rest import Client

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
    session['contact'] = contact
    return redirect(url_for('.verify_contact', contact=contact))

@app.route('/verify', methods=['POST', 'GET'])
def verify_contact():
    client = Client(AC_SID, AUTH_TOKEN)
    verify = client.verify.services(VERIFY)
    contact = request.args['contact']
    contact = session['contact']
    contact = '+' + contact

    if request.method == 'POST':
        verify.verifications.create(to=contact, channel='sms')
        try:
            code = request.form["code"]
        except Exception as e:
            return e
        try:
            result = verify.verification_checks.create(to=contact, code=code)
        except:
            return e
        if (result.status == 'approved'):
            return redirect('/')
        else:
            return "Invalid Token"
    else:
        verify.verifications.create(to=contact, channel='sms')
        return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
