import pandas as pd
from sqlalchemy import Column, String, create_engine,INTEGER
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import *
from config import SQLALCHEMY_DATABASE_URI

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
