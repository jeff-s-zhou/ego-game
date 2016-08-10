__author__ = 'Jeffrey'

from sqlalchemy import Column, Integer, Text, Boolean, DateTime

from shared import db

class Character(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    account_id = Column(Integer, unique=False)
    hp = Column(Integer, unique=False)
    power = Column(Integer, unique=False)
    defense = Column(Integer, unique=False)
    initiative = Column(Integer, unique=False)

class Skills(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)

class Character_Skills(db.Model):
    id = Column (Integer, primary_key=True)
    character_id = Column(Integer, unique=False)
    skill_id = Column(Integer, unique=False)