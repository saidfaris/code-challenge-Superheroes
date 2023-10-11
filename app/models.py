from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func
from sqlalchemy.orm import relationship, validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(DateTime, default=func.now())
    updated_at = db.Column(DateTime, onupdate=func.now())
    powers = relationship("HeroPowers", backref='hero')

    serialize_rules = ('-powers.hero', )
class HeroPowers(db.Model, SerializerMixin):
    __tablename__ = 'heropowers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(DateTime, default=func.now())
    updated_at = db.Column(DateTime, onupdate=func.now())
    serialize_rules = ('-power.heroes', '-hero.powers')
    def __init__(self, strength, hero_id, power_id):
        self.strength = strength
        self.hero_id = hero_id
        self.power_id = power_id


    @validates('strength')
    def validate_strength(self, key, strength):
        assert strength in ['Strong', 'Weak', 'Average'], "Strength must be one of the following values: 'Strong', 'Weak', 'Average'"
        return strength

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    created_at = db.Column(DateTime, default=func.now())
    updated_at = db.Column(DateTime, onupdate=func.now())
    heroes = relationship("HeroPowers", backref='power')
    serialize_rules = ('-heroes.power',)
    @validates('description')
    def validate_description(self, key, description):
        assert description and len(description) >= 20, "Description must be present and at least 20 characters long"
        return description

