# backend/app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 允许前端跨域访问
import os

app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'students.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '123456'


db = SQLAlchemy(app)

# ---------------- 模型定义 ----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    fzu_num = db.Column(db.String(10))
    miec_num = db.Column(db.String(10))
    phone_num = db.Column(db.String(10))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# ---------------- 接口定义 ----------------

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'status': 'fail', 'msg': 'The user already exists.'})

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'success', 'msg': 'Registration successful.'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({'status': 'success', 'msg': 'Login successful.'})
    else:
        return jsonify({'status': 'fail', 'msg': 'Username or password is incorrect.'})

@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    result = [
        {'id': s.id, 'name': s.name, 'fzu_num': s.fzu_num, 'miec_num': s.miec_num, 'phone_num': s.phone_num}
        for s in students
    ]
    return jsonify(result)

@app.route('/api/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    new_stu = Student(
        name=data.get('name'),
        fzu_num=data.get('fzu_num'),
        miec_num=data.get('miec_num'),
        phone_num=data.get('phone_num')
    )
    db.session.add(new_stu)
    db.session.commit()
    return jsonify({'status': 'success', 'msg': 'Added successfully'})

@app.route('/api/delete_student', methods=['POST'])
def delete_student():
    data = request.get_json()
    name = data.get('name')
    stu = Student.query.filter_by(name=name).first()
    if stu:
        db.session.delete(stu)
        db.session.commit()
        return jsonify({'status': 'success', 'msg': f'Have deleted {name}'})
    return jsonify({'status': 'fail', 'msg': 'The member does not exist'})

@app.route('/api/update_student', methods=['POST'])
def update_student():
    data = request.get_json()
    old_name = data.get('old_name')
    stu = Student.query.filter_by(name=old_name).first()
    if stu:
        stu.name = data.get('name')
        stu.fzu_num = data.get('fzu_num')
        stu.miec_num = data.get('miec_num')
        stu.phone_num = data.get('phone_num')
        db.session.commit()
        return jsonify({'status': 'success', 'msg': 'Modified successfully'})
    return jsonify({'status': 'fail', 'msg': 'The member does not exist'})

if __name__ == '__main__':
    app.run()