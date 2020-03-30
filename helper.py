import models
from flask import request, render_template, url_for
import pickle
import sys
from werkzeug.security import generate_password_hash, check_password_hash
import collections




class DBtool:
    def __init__(self, db):
        self.db = db

class UserTool(DBtool):
    def __init__(self, db,uid):
        super().__init__(db)
        self.uid=uid

    def addSkill(self,skillContext):
        skill_id = models.Skill.query.filter_by(skill_context=skillContext).first()
        if not skill_id:
            pass
        if not self.isSkillExsist(skillID=skill_id.id):
            skill_id = int(skill_id.id)
            dbUserSkill=models.UserSkills(user_id=self.uid,skill_id=skill_id)
            self.db.session.add(dbUserSkill)
            self.db.session.commit()

    def addSkillFromCourse(self,courseNameList):
        for courseName in courseNameList:
            course_id = models.Course.query.filter_by(name=courseName).first()
            if course_id:
                for courseSkill in course_id.course_skill:
                    skillTableSkill=models.Skill.query.filter_by(id=courseSkill.skill_id).first()
                    if not self.isSkillExsist(skillID=skillTableSkill.id):
                        dbUserSkill = models.UserSkills(user_id=self.uid, skill_id=skillTableSkill.id)
                        self.db.session.add(dbUserSkill)
                        self.db.session.commit()

    def isSkillExsist(self,skillID):
        skillTableSkill = models.UserSkills.query.filter_by(user_id=self.uid,skill_id=skillID).first()
        if skillTableSkill:
            return True
        return False

    def findIntership(self):
        userSkills=models.UserSkills.query.filter_by(user_id=self.uid).all()
        # jobIDList=[]
        jobCounter=collections.Counter()
        returnJobs=[]
        if not userSkills:
            return []
        for userSkill in userSkills:
            skill_id=userSkill.skill_id
            matchedSkills=models.JobSkill.query.filter_by(skill_id=skill_id).all()
            for matchedSkill in matchedSkills:
                jobPost=models.JobPost.query.filter_by(id=matchedSkill.job_post_id).first()
                if jobPost.id:
                    # jobIDList.append(jobPost.id)
                    jobCounter.update([jobPost.id])

        for key,count in jobCounter.most_common():
            jobPost = models.JobPost.query.filter_by(id=key).first()
            jobCompany = models.Company.query.filter_by(id=jobPost.company_id).first()
            returnJobs.append({
                "job_name": jobPost.name,
                "company": jobCompany.name,
                "job_id":key
            })

        return returnJobs

    def jobDetail(self,jobID):
        jobPost = models.JobPost.query.filter_by(id=jobID).first()
        jobCompany = models.Company.query.filter_by(id=jobPost.company_id).first()
        requirements=models.JobRequirement.query.filter_by(job_post_id=jobPost.id).all()
        requirementList=[]
        for requirement in requirements:
            requirementList.append({
                "context":requirement.context
            })
        context={
            "job_name":jobPost.name,
            "company_name":jobCompany.name,
            "requirements":requirementList
        }
        return context




class FormandDbtool:
    def __init__(self, form, db):
        self.form = form
        self.db = db


class SignUpHelper(FormandDbtool):
    def SignUp(self):
        form = self.form
        db = self.db
        username = form.get('username')
        password = form.get('password')
        confirm_password = request.form.get('confirm_password')
        context = {
            'username_valid': 0,
            'password_valid': 0,
            'pawconfirm_valid': 0,
            'username': username
        }

        flag = False
        if not 2 <= len(username) <= 100:
            context['username_valid'] = 1
            flag = True

        if password != confirm_password:
            context['password_valid'] = 1
            flag = True

        if not 2 <= len(password) <= 100:
            context['password_valid'] = 2
            flag = True

        # users are not allowed to have same username
        dup_user = models.User.query.filter_by(username=username).first()
        if dup_user:
            context['username_valid'] = 2
            flag = True

        if flag:
            return render_template('signup.html', **context)

        # Different users are allowed to have the same password
        # After using salt value for storing passwords, they will look completely different on the server(database)
        # even though they are the same
        password = generate_password_hash(password + username)
        candidate_user = models.User(username=username, password=password)
        db.session.add(candidate_user)
        db.session.commit()
        # two directories are created to store the images later uploaded by the user
        # log in
        return (username, candidate_user.id)
