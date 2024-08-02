from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_font_awesome import FontAwesome

app = Flask(__name__)
font_awesome = FontAwesome(app)     #pip install Font-Awesome-Flask (https://github.com/sgraaf/font-awesome-flask) https://flask.palletsprojects.com/en/latest/
db_name = "Students"
app.secret_key = 'students flask app' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://.\sqlexpress/' + db_name + '?driver=SQL+Server' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Сущность 'Студент'
class Student(db.Model):
    __tablename__ = "Student"
    id = Column(Integer, primary_key = True)    
    name = Column(String(50))
    phone = Column(String(50))
    card = Column(String(15))  
    group = relationship('StudentGroup', backref = 'Student')     
    groupId = Column(Integer, ForeignKey('StudentGroup.id'))

# Сущность 'Студенческая группа'
class StudentGroup(db.Model):
    __tablename__ = "StudentGroup"
    id = Column(Integer, primary_key = True)    
    name = Column(String(15))
    chief = Column(Integer, nullable = True)
    department = relationship('Department', backref = 'StudentGroup')       
    deptId = Column(Integer, ForeignKey('Department.id'))

# Сущность 'Кафедра'
class Department(db.Model):
    __tablename__ = "Department"
    id = Column(Integer, primary_key = True)    
    name = Column(String(15))
    
# Сущность 'Пользователь'
class User(db.Model):
    __tablename__ = "User"    
    id = db.Column(Integer, primary_key = True)
    username = db.Column(String(50), unique = True, nullable = False)
    password = db.Column(String(50), nullable = False)  
    role = db.Column(String(20), nullable = False)  
