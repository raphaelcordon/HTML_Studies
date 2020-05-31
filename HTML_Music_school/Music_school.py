from db import CourseDB, UsersDB, DeletingDB, FindId, Authenticate
from flask import Flask, render_template, redirect, request, url_for, flash, session
from models import Course, Users, Edit_Users_Access_Level, ACCESS_LEVEL


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    return render_template('index.html')


# <--- Course routes beginning --->
@app.route('/course')
def course():
    course_list = CourseDB.course_list()
    return render_template('course.html', title='Course List', course=course_list)


@app.route('/CourseRegistry', methods=['POST',])
def course_registry():
    name = str(request.form['name']).strip().title()
    if name == '':
        flash('Blank field not accepted')
    elif CourseDB.course_new(name):
        flash('Already registered, please check below')
    else:
        flash('Successfully created')
    return redirect(url_for('course'))


@app.route('/CourseEdit/<category>/<int:id>')
def course_edit(category, id):
    data = CourseDB.course_find_id(category, id)
    return render_template('edit_course.html', data=data, category=category)


@app.route('/CourseUpdate', methods=['POST',])
def course_update():
    id = request.form['id']
    name = str(request.form['name']).strip().title()
    course = Course(id, name)
    if name == '':
        flash('Blank field not accepted')
    elif CourseDB.course_update(course.id, course.name):
        flash('Already registered, please check below')
    else:
        flash('Successfully updated')
    return redirect(url_for('course'))

# <--- Course routes ending --->


# <--- Users routes beginning --->

@app.route('/users')
def users():
    users_list = UsersDB.users_list()
    return render_template('users.html', title='Users List', users=users_list, ACCESS_LEVEL=ACCESS_LEVEL)


@app.route('/UsersRegistry', methods=['POST',])
def users_registry():
    name = str(request.form['name']).strip().title()
    password = 'pass'
    course = 0
    access_level = request.form['access_level']

    if name == '' or access_level == '':
        flash('Blank field not accepted')
    elif UsersDB.users_new(name, password, course, access_level):
        flash('Already registered, please check below')
    else:
        flash("Successfully created. User the password 'pass' to login for the first time.")
    return redirect(url_for('users'))


@app.route('/UsersEdit/<category>/<int:id>')
def users_edit(category, id):
    data = UsersDB.users_find_id(category, id)
    return render_template('edit_users.html', data=data, category=category, ACCESS_LEVEL=ACCESS_LEVEL)


@app.route('/UsersUpdate', methods=['POST',])
def users_update():
    id = request.form['id']
    name = str(request.form['name']).strip().title()
    access_level = request.form['access_level']
    users = Edit_Users_Access_Level(id, name, access_level)
    print(users.id, users.name, users.access_level)
    if name == '':
        flash('Blank field not accepted')
    elif UsersDB.users_update(users.id, users.name, users.access_level):
        flash('Already registered, please check below')
    else:
        flash('Successfully updated')
    return redirect(url_for('users'))

# <--- Users routes ending --->

@app.route('/Delete/<int:id>/<category>')
def Delete(category, id):
    DeletingDB(category, id)
    flash('Successfully removed')
    return redirect(url_for(f'{category}'))


@app.route('/authenticate', methods=['POST',])
def authenticate():
    user = Authenticate.authenticate(request.form['name'])
    if user.password == request.form['pass']:
        session['user_logged'] = user.id
        flash(f'{user.nome} is logged in')
        return redirect('index')
    else:
        flash('Login failed, please try again')
        return redirect('/')


@app.route('/logout')
def logout():
    session['user_logged'] = None
    flash('Loggeed out!')
    return redirect(url_for('index'))

app.run(debug=True)