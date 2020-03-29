import pandas as pd

dfJob=pd.read_csv("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/static/data/job_describtion.csv",header=None,dtype=str)
dfJobDes=pd.read_csv("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/static/data/job_requirement_describtion.csv",header=None,dtype=str)
dfSkill=pd.read_csv("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/static/data/skills_clean.csv",header=0,dtype=str)

n=len(dfSkill)
skillList=[]
for i in range(n):
    row=dfSkill.iloc[i]
    skillList.append(str(row['skill']))

def re2(a):
    return a[1]

# skillList.sort(key=re2,reverse=True)

n=len(dfJob)
print(skillList[0])
print(dfJob.iloc[0])
print(dfJobDes.iloc[0])
for i in range(1):
    row=dfJob.iloc[i]
    jobID=str(row[0])
    url=str(row[0])
    if "https://ca.indeed.com" not in url:
        url="https://ca.indeed.com"+url
    jobName=str(row[2])
    companyName=str(row[3])
    dfSingleJobDes=dfJobDes[dfJobDes[1]==jobID]
    lenDes = len(dfSingleJobDes)
    desList=[]
    requireSkillList=[]
    for j in range(lenDes):
        jobDescription=dfSingleJobDes.iloc[j][2]
        desList.append(jobDescription)
        for skill in skillList:
            if (skill not in requireSkillList):
                if ((' ' in skill) and (skill.lower() in jobDescription.lower())) or ((' ' not in skill) and (skill.lower() in jobDescription.lower().split(' '))):
                    requireSkillList.append(skill)

    print(desList)
    print(requireSkillList)