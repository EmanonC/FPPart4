import pandas as pd
from sqlalchemy import Column, String, create_engine,INTEGER
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import *
from config import SQLALCHEMY_DATABASE_URI


db = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding='utf-8', echo=True)
DBSession = sessionmaker(bind=engine)
db = DBSession()
skillTableSkill=db.query(Skill).all()
for s in skillTableSkill:
    print(s.skill_context)