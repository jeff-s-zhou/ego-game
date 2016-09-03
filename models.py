__author__ = 'Jeffrey'

from sqlalchemy import Column, Integer, Text, Boolean, DateTime

from shared import db

class Character(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    account_id = Column(Integer)
    hp = Column(Integer)
    power = Column(Integer)
    defense = Column(Integer)
    initiative = Column(Integer)

class Skill(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    description = Column(Text)
    cooldown = Column(Integer)
    valid = Column(Boolean)

class CharacterSkill(db.Model):
    id = Column (Integer, primary_key=True)
    character_id = Column(Integer)
    skill_id = Column(Integer)