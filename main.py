from flask import Flask, g, request, render_template, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from entities import app, db, Student, StudentGroup, Department, User
from waitress import serve

user_role = None


""" Студенты """

# Роут для отображения и актуализации информации о всех студентах
@app.route('/students', methods = ['GET'])
def students():
    students = db.session.query(Student).order_by(Student.name.asc()).all()
    groups = db.session.query(StudentGroup).order_by(StudentGroup.name.asc()).all()
    if user_role is not None:
        return render_template('students_part.html', students = students, groups = groups, role = user_role) 
    else:
        return render_template('login.html')    

# Функция возвращает True, если студент существует в БД и False, если нет 
def is_student_exists(name, phone, card, group_id):
    if db.session.query(Student).filter((Student.name == name) &
                        (Student.phone == phone) &
                        (Student.card == card) &
                        (Student.groupId == int(group_id))).count() > 0: 
        return True
    else:
        return False  
    
# Функция возвращает id для существующего студента 
def get_student_id(name, phone, card, group_id):
    student = db.session.query(Student).filter((Student.name == name) &
                    (Student.phone == phone) &
                    (Student.card == card) &
                    (Student.groupId == int(group_id))).first()
    return student.id

# Роут для добавления студента
@app.route('/addstudent', methods = ['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_name = request.form['name']
        student_phone = request.form['phone']
        student_card = request.form['card']
        group_id = int(request.form['groupId'])
        if "chief" in request.form:
            group_chief = request.form['chief']
        
        if not is_student_exists(student_name, student_phone, student_card, group_id):     
            db.session.add(Student(name = student_name, 
                           phone = student_phone,
                           card = student_card,
                           groupId = group_id))
            db.session.commit() 
            # Студент - староста группы
            if "chief" in request.form and group_chief == "on":
                student_id = get_student_id(student_name, student_phone, student_card, group_id)
                db.session.query(StudentGroup).get(group_id).chief = student_id   
                db.session.commit()         
            msg = "not_exists"
        else:
            msg = "exists" 
             
    return redirect(url_for('students') + '?msg=' + msg)

# Роут для изменения студента (студентов)
@app.route('/alterstudent', methods = ['GET', 'POST'])
def alter_student():
    if request.method == 'POST':
        student_id = int(request.values.get('id'))        
        student_name = request.values.get('name')
        student_phone = request.values.get('phone')
        student_card = request.values.get('card')
        group_id = int(request.values.get('groupId'))
        group_chief = request.values['chief']        
   
        if not is_student_exists(student_name, student_phone, student_card, group_id):  
            student = db.session.query(Student).get(student_id)  
            if student.name != student_name:
                student.name = student_name    
            if student.phone != student_phone:
                student.phone = student_phone    
            if student.card != student_card:
                student.card = student_card     
            if student.groupId != group_id:
                student.groupId = group_id 
            # Студент - староста группы
            if group_chief == "on":
                db.session.query(StudentGroup).get(group_id).chief = student_id 
            db.session.commit()              
            msg = "not_exists"
        else:
            if group_chief == "on" and is_chief(student_id, group_id) or group_chief == "off" and not is_chief(student_id, group_id):
                msg = "exists"   
            else:              
                group = db.session.query(StudentGroup).filter((StudentGroup.chief == student_id)).first()   
                # Студент - староста группы
                if group_chief == "on" and group == None:
                    db.session.query(StudentGroup).get(group_id).chief = student_id 
                # Студент - не староста группы                
                if group_chief == "off" and group != None:
                    group.chief = None  
                db.session.commit() 
                msg = "not_exists"                                                                                                                   

    return jsonify({"msg": msg})

# Функция возвращает True, если студент является старостой группы и False, если нет 
def is_chief(student_id, group_id):
    group = db.session.query(StudentGroup).filter((StudentGroup.id == group_id)).first()    
    return group.chief == student_id

# Роут для удаления студента (студентов)
@app.route('/removestudent', methods = ['GET', 'POST'])
def remove_student():
    if request.method == 'POST':
        student_id = int(request.values.get('id')) 
        if "chief" in request.values and request.values['chief'] == "on":
            group = db.session.query(StudentGroup).filter((StudentGroup.chief == student_id)).first()  
            group.chief = None  
            db.session.commit()        
              
        db.session.query(Student).filter(Student.id == student_id).delete()
        db.session.commit()

    return redirect(url_for('students'))



""" Группы """

# Роут для отображения и актуализации информации о всех студенческих группах
@app.route('/groups', methods = ['GET'])
def groups():
    groups = db.session.query(StudentGroup).order_by(StudentGroup.name.asc()).all() 
    departments = db.session.query(Department).order_by(Department.name.asc()).all()     

    if user_role is not None:
        return render_template('groups_part.html', groups = groups, departments = departments, role = user_role)  
    else:
        return render_template('login.html')    

# Функция возвращает True, если группа существует в БД и False, если нет 
def is_group_exists(name, dept_id):
    if db.session.query(StudentGroup).filter((StudentGroup.name == name) &
                       (StudentGroup.deptId == int(dept_id))).count() > 0: 
        return True
    else:
        return False 

# Роут для добавления группы
@app.route('/addgroup', methods = ['GET', 'POST'])
def add_group():
    if request.method == 'POST':
        group_name = request.form['name']
        dept_id = request.form['deptId']

        if not is_group_exists(group_name, dept_id):     
            db.session.add(StudentGroup(name = group_name, chief = None, deptId = dept_id))
            db.session.commit() 
            msg = "not_exists"
        else:
            msg = "exists" 
             
    return redirect(url_for('groups') + '?msg=' + msg)        

# Роут для изменения группы (групп)
@app.route('/altergroup', methods = ['GET', 'POST'])
def alter_group():
    if request.method == 'POST':
        group_id = int(request.values.get('id'))        
        group_name = request.values.get('name')
        dept_id = int(request.values.get('deptId'))

        if not is_group_exists(group_name, dept_id):  
            group = db.session.query(StudentGroup).get(group_id)  
            if group.name != group_name:
                group.name = group_name     
            if group.deptId != dept_id:
                group.deptId = dept_id  
            db.session.commit()  
            msg = "not_exists"
        else:
            msg = "exists"                                                                                        

    return jsonify({"msg": msg})

# Роут для удаления группы (групп)
@app.route('/removegroup', methods = ['GET', 'POST'])
def remove_group():
    if request.method == 'POST':
        group_id = request.values.get('groupId')     
              
        if db.session.query(Student).filter((Student.groupId == int(group_id))).count() > 0: 
            msg = "not_remove_" + group_id
        else:
            db.session.query(StudentGroup).filter(StudentGroup.id == int(group_id)).delete()
            db.session.commit()
            msg = "remove"                                                                                        

    return jsonify({"msg": msg})

# Удаление группы из БД
@app.route('/do_remove_group', methods = ['GET', 'POST'])
def do_remove_group():
    if request.method == 'POST':
        group_id = request.values.get('groupId')   
    db.session.query(StudentGroup).filter(StudentGroup.id == int(group_id)).delete()
    db.session.commit()
    return redirect(url_for('groups')) 



""" Кафедры """

# Роут для отображения и актуализации информации о всех кафедрах
@app.route('/departments', methods = ['GET'])
def departments():
    departments = db.session.query(Department).order_by(Department.name.asc()).all()     

    if user_role is not None:
        return render_template('departments_part.html', departments = departments, role = user_role)  
    else:
        return render_template('login.html')    

# Функция возвращает True, если кафедра присутствует в БД и False, если нет 
def is_department_exists(name):
    if db.session.query(Department).filter(Department.name == name).count() > 0: 
        return True
    else:
        return False 
    
# Роут для добавления кафедры
@app.route('/adddepartment', methods = ['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        department_name = request.form['name']

        if not is_department_exists(department_name):     
            db.session.add(Department(name = department_name))
            db.session.commit() 
            msg = "not_exists"
        else:
            msg = "exists" 
             
    return redirect(url_for('departments') + '?msg=' + msg)  

# Роут для изменения кафедры (кафедр)
@app.route('/alterdepartment', methods = ['GET', 'POST'])
def alter_department():
    if request.method == 'POST':
        department_id = int(request.values.get('id'))        
        department_name = request.values.get('name')

        if not is_department_exists(department_name):  
            department = db.session.query(Department).get(department_id)  
            if department.name != department_name:
                department.name = department_name     
            db.session.commit()  
            msg = "not_exists"
        else:
            msg = "exists"                                                                                        

    return jsonify({"msg": msg}) 

# Роут для удаления кафедры (кафедр)
@app.route('/removedepartment', methods = ['GET', 'POST'])
def remove_department():
    if request.method == 'POST':
        department_id = request.values.get('departmentId')     
              
        if db.session.query(Department).filter((StudentGroup.deptId == int(department_id))).count() > 0: 
            msg = "not_remove_" + department_id
        else:
            db.session.query(Department).filter(Department.id == int(department_id)).delete()
            db.session.commit()
            msg = "remove"                                                                                        

    return jsonify({"msg": msg})

# Удаление кафедры из БД
@app.route('/do_remove_department', methods = ['GET', 'POST'])
def do_remove_department():
    if request.method == 'POST':
        department_id = request.values.get('departmentId')   
    db.session.query(Department).filter(Department.id == int(department_id)).delete()
    db.session.commit()
    return redirect(url_for('departments')) 



""" Регистрация """

# Функция возвращает True, если в БД существует пользователь с таким же логином и False, если нет 
def is_user_exists(username):
    if db.session.query(User).filter(User.username == username).count() > 0: 
        return True
    else:
        return False 
    
# Роут для отображения формы регистрации
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        hashed_password = generate_password_hash(password, method = 'scrypt')      
        role = request.values.get('role')

        if not is_user_exists(username):     
            new_user = User(username = username, password = hashed_password, role = role)
            db.session.add(new_user)
            db.session.commit()
            msg = "not_exists"
        else:
            msg = "exists" 

        return jsonify({"msg": msg}) 
    
    if user_role is not None and user_role == "admin" :
        users = db.session.query(User).order_by(User.username.asc()).all() 
        return render_template('register.html', users = users, role = user_role) 
    else:
        return render_template('login.html')   

# Роут для удаления пользователя
@app.route('/removeuser', methods = ['GET', 'POST'])
def removeuser():
    if request.method == 'POST':
        user_id = request.values.get('id')

        db.session.query(User).filter(User.id == int(user_id)).delete()
        db.session.commit()
    
        if user_role is not None:
            users = db.session.query(User).order_by(User.username.asc()).all() 
            return render_template('register.html', users = users, role = user_role) 
        else:
            return render_template('login.html')                

# Роут для входа в приложение
@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()

        global user_role 
        if bool(user):
            user_role = user.role
        else:
            user_role = None

        if user and check_password_hash(user.password, password):
            return redirect(url_for('students'))   

    return render_template('login.html')

# Роут для выхода в приложение
@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    global user_role 
    user_role = None

    return render_template('login.html')

""" О приложении """


@app.route('/home')
def home():
    return render_template('home.html', role = user_role)

if __name__ == '__main__':
    app.run(host = "127.0.0.1", port = 5050, debug = True)
    # serve(app, host = "127.0.0.1", port = 5050)