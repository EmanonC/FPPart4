from flask import render_template, flash, request, redirect, url_for, session, jsonify, Flask
import models
from exts import db
import config, datetime, pymysql
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os
from sql_tool import *
from helper import *

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app=app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('user'))

    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    # login page
    # verify the username and password provided by the user
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        candidate_user = models.User.query.filter_by(username=username).first()
        uid = candidate_user.id
        try:
            candidate_user.username
        except:
            return render_template('login.html', p=1)
        if check_password_hash(candidate_user.password, password + username):
            session['user'] = username
            session['uid'] = uid
            session.permanent = True
            # after 24 hours, users are required to reenter their usernames and passwords for security purposes
            app.permanent_session_lifetime = timedelta(minutes=1440)
            return redirect(url_for('user', username=username))
        else:
            flash('Invalid username or password')
            return render_template('login.html', p=1)
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # registration page
    # On the server side, check whether the username and password are valid or not.
    # username and password must be strings between 2 to 100 characters
    if request.method == "POST":
        SignUp=SignUpHelper(form=request.form,db=db)
        session['user'],session['uid']=SignUp.SignUp()
        return redirect(url_for('user'))
    context = {
        'username_valid': -1,
        'password_valid': -1,
        'pawconfirm_valid': -1
    }
    return render_template('signup.html', **context)


@app.route('/user', methods=["GET", "POST"])
def user():
    # if the user are not logged in, redirect to the login page
    if 'user' not in session:
        return redirect(url_for('index'))
    username = session['user']
    return render_template('user.html', user=username)

@app.route('/addskill', methods=["GET", "POST"])
def addSkill():
    # if the user are not logged in, redirect to the login page
    if 'user' not in session:
        return redirect(url_for('index'))
    username = session['user']
    uid = session['uid']
    if request.method == 'GET':
        context={}
        return render_template('add_skill.html', **context)

    else:
        try:
            skillNames = request.form.getlist('skillName')
            for skillName in skillNames:
                try:
                    userTool=UserTool(db=db,uid=uid)
                    userTool.addSkill(skillContext=skillName)
                    context = {}
                except:
                    context = {}
                    pass
            return redirect(url_for('findLocation'))
        except:
            return render_template('add_skill.html', **context)

@app.route('/findjob', methods=["GET", "POST"])
def findJob():
    # if the user are not logged in, redirect to the login page
    if 'user' not in session:
        return redirect(url_for('index'))
    # username = session['user']
    uid=session['uid']
    userTool = UserTool(db=db, uid=uid)
    jobs=userTool.findIntership()
    # context = data.getContextforAdding()
    context={
        'jobs':jobs[:15],
    }
    return render_template('job_list_view.html', **context)

@app.route('/viewskills', methods=["GET", "POST"])
def viewAllSkills():
    # if the user are not logged in, redirect to the login page
    if 'user' not in session:
        return redirect(url_for('index'))
    # username = session['user']
    uid=session['uid']
    userTool = UserTool(db=db, uid=uid)
    context=userTool.skillViewContext()
    return render_template('view_user_skills.html', **context)

@app.route('/location')
def findLocation():
    return render_template('location_selection.html')


@app.route('/jobdetail', methods=["GET", "POST"])
def jobDetail():
    # if the user are not logged in, redirect to the login page
    if 'user' not in session:
        return redirect(url_for('index'))
    # username = session['user']
    uid=session['uid']
    userTool = UserTool(db=db, uid=uid)
    jobID=request.args.get('job_id')
    context=userTool.jobDetail(jobID=jobID)
    return render_template('job_detail.html', **context)


@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    uid = session['uid']
    context={}
    if request.method == "POST":
        try:
            file = request.files['resume']
            # file.save(f"/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/UserData/{uid}/resume.pdf")
            file_name=os.path.join("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/UserData", f"{uid}resume.pdf")
            file.save(file_name)
            userTool = UserTool(db=db, uid=uid)
            userTool.addSkillFromPDFFile(filename=file_name)
            context.update({'msg':"Success!"})

        except:
            pass
    return render_template('upload_resume.html',**context)


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    context = {}
    if request.method == "POST":
        try:
            uid = session['uid']
            course_names = request.form.getlist('skillName')
            userTool = UserTool(db=db, uid=uid)
            userTool.addSkillFromCourse(courseNameList=course_names)
            context.update({'msg': "Success!"})
        except:
            context.update({'msg': "Course Not Found"})
            pass
    return render_template('add_course.html',**context)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))



#Scriptes start

@app.route('/scripts')
def scripts():
    contex = {
        'msg': 'Scripts'
    }
    return render_template('scripts.html', **contex)

@app.route('/scripts/uploadskill')
def uploadSkill():
    Tool=indeed_data_importer(db=db)
    Tool.upload_skills()
    contex = {
        'msg': 'Success'
    }
    return render_template('scripts.html', **contex)


@app.route('/scripts/uploadjob')
def uploadJob():
    Tool=indeed_data_importer(db=db)
    Tool.upload_jobs()
    contex = {
        'msg': 'Success'
    }
    return render_template('scripts.html', **contex)



if __name__ == '__main__':
    app.run(debug=True)
