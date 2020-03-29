import pandas as pd

dfJob=pd.read_csv("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/static/data/job_describtion.csv",header=None)
dfJobDes=pd.read_csv("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/static/data/job_requirement_describtion.csv",header=None)
dfSkill=pd.read_csv("/Users/yilunhuang/Desktop/Grad/MIE1624/FPPart4/static/data/skills_clean.csv",header=0)

n=len(dfSkill)
skillList=[]
for i in range(n):
    row=dfSkill.iloc[i]
    skillList.append([row['skill'],row['count']])

def re2(a):
    return a[1]

skillList.sort(key=re2,reverse=True)
print(skillList)