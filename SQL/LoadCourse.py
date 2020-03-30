import pandas as pd
from sqlalchemy import Column, String, create_engine,INTEGER
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import *
from config import SQLALCHEMY_DATABASE_URI

dfJob = pd.read_csv("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/static/data/job_describtion.csv", header=None)
dfJobDes = pd.read_csv("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/static/data/job_requirement_describtion.csv",
                       header=None)
dfSkill = pd.read_csv("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/static/data/skills_clean.csv", header=0)
dfCourese = pd.read_csv("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/static/data/course_vs_skills.csv", header=0)

db = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding='utf-8', echo=True)
DBSession = sessionmaker(bind=engine)
db = DBSession()

print(dfCourese['name'])
n = len(dfCourese)
for i in range(n):
    row=dfCourese.iloc[i]
    # print(row['name'],row['topics'].split('/'))
    courseName=row['name']
    skillList=row['topics'].split('/')
    dbCourse=Course(name=courseName)
    db.add(dbCourse)
    db.commit()
    courseID=dbCourse.id
    for skilli in skillList:
        skillTableSkill=db.query(Skill).filter(Skill.skill_context==skilli).first()
        if skillTableSkill:
            skillID=skillTableSkill.id
            dbCourseSkill=CourseSkill(course_id=courseID,skill_id=skillID)
            db.add(dbCourseSkill)
            db.commit()

# a=db.query(JobSkill).filter(JobSkill.skill_id==1250).all()
# print(a[0].id)
# IndeedJob=IndeedJobTable(herf=herf,job_type=job_type)
# self.db.add(IndeedJob)
# self.db.commit()