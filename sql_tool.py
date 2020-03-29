import models
from flask import request, render_template, url_for
import pickle
import sys
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd


class indeed_data_importer:
    def __init__(self, db):
        self.db = db

    def upload_jobs(self):
        dfJob = pd.read_csv("/Users/jackzhang/Desktop/projects/FPPart4/static/data/job_describtion.csv",
                            header=None, dtype=str)
        dfJobDes = pd.read_csv(
            "/Users/jackzhang/Desktop/projects/FPPart4/static/data/job_requirement_describtion.csv", header=None,
            dtype=str)
        dfSkill = pd.read_csv("/Users/jackzhang/Desktop/projects/FPPart4/static/data/skills_clean.csv", header=0,
                              dtype=str)

        n = len(dfSkill)
        skillList = []
        for i in range(n):
            row = dfSkill.iloc[i]
            skillList.append(str(row['skill']))


        n = len(dfJob)
        for i in range(n):
            row = dfJob.iloc[i]
            jobID = str(row[0])
            url = str(row[0])
            if "https://ca.indeed.com" not in url:
                url = "https://ca.indeed.com" + url
            jobName = str(row[2])
            companyName = str(row[3])
            companyDB = models.Company.query.filter_by(name=companyName).first()
            if not companyDB:
                dbCompany=models.Company(name=companyName)
                self.db.session.add(dbCompany)
                self.db.session.commit()
                companyID=dbCompany.id
            else:
                companyID=companyDB.id
            companyID=int(companyID)

            dfSingleJobDes = dfJobDes[dfJobDes[1] == jobID]
            lenDes = len(dfSingleJobDes)
            desList = []
            requireSkillList = []

            dbJob=models.JobPost(name=jobName,href=url,requirement_num=lenDes,company_id=companyID)
            self.db.session.add(dbJob)
            self.db.session.commit()
            jobPostID = dbJob.id

            for j in range(lenDes):
                jobDescription = str(dfSingleJobDes.iloc[j][2])
                desList.append(jobDescription)
                dbJobDescription=models.JobRequirement(context=jobDescription,job_post_id=jobPostID)
                self.db.session.add(dbJobDescription)
                self.db.session.commit()
                for skill in skillList:
                    if (skill not in requireSkillList):
                        if ((' ' in skill) and (skill.lower() in jobDescription.lower())) or (
                                (' ' not in skill) and (skill.lower() in jobDescription.lower().split(' '))):
                            requireSkillList.append(skill)
                            skill_id=models.Skill.query.filter_by(skill_context=skill).first()
                            skill_id=int(skill_id.id)
                            dbJobSkill=models.JobSkill(job_post_id=jobPostID,skill_id=skill_id)
                            self.db.session.add(dbJobSkill)
                            self.db.session.commit()


    def upload_skills(self):
        dfSkill = pd.read_csv("/Users/jackzhang/Desktop/projects/FPPart4/static/data/skills_clean.csv", header=0)
        n = len(dfSkill)
        skillList = []
        for i in range(n):
            row = dfSkill.iloc[i]
            skillList.append([row['skill'], row['count']])
        # def re2(a):
        #     return a[1]
        # skillList.sort(key=re2, reverse=True)
        for skill in skillList:
            dbskill = models.Skill(skill_context=str(skill[0]), skill_score=str(skill[1]))
            self.db.session.add(dbskill)
            self.db.session.commit()
