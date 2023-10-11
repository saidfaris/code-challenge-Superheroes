#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api, Resource


from models import Hero, HeroPowers, Power,db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route('/')
def home():
    return ''

class HeroesInfo(Resource):

    def get(self):
        Heros = []
        for hero in Hero.query.all():
            hero_dict = hero.to_dict()
            Heros.append(hero_dict)
        
        print(Heros)

        response = make_response(
            jsonify(Heros),200
        )
        return response
api.add_resource(HeroesInfo, '/heroes')
class HerosId (Resource):
    def get(self,id):
        hero = Hero.query.filter_by(id=id).first()
        if hero is None:
            return make_response(jsonify({'error':'Hero not found'}),404)

        else:
            hero_dict = hero.to_dict()
            response = make_response(
            jsonify(hero_dict),200
            )
            return response

api.add_resource(HerosId, '/heroes/<int:id>')

class Getpowers(Resource):
   def get(self):
        powers = []
        for power in Power.query.all():
            power_dict = power.to_dict()
            powers.append(power_dict)
        
        print(powers)

        response = make_response(
            jsonify(powers),200
        )
        return response
api.add_resource(Getpowers,'/powers')

class PowerId (Resource):
    def get(self,id):
        power = Power.query.filter_by(id=id).first()
        if power is None:
            return make_response(jsonify({'error':'Power not found'}),404)

        else:
            power_dict = power.to_dict()
            response = make_response(
            jsonify(power_dict),200
            )
            return response

    def patch(self, id):
        power = Power.query.filter_by(id=id).first()
        if power is None:
            return make_response(jsonify({'error': 'Power not found'}), 404)
        else:
            data = request.get_json()
            if 'description' in data:
                power.description = data['description']
                db.session.commit()
                return make_response(jsonify(power.to_dict()), 200)
            else:
                return make_response(jsonify({'errors': ['validation errors']}), 400)

api.add_resource(PowerId, '/powers/<int:id>')

class HeroPowers(Resource):
    def post(self):
        data = request.get_json()
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')
        strength = data.get('strength')

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if hero is None or power is None:
            return make_response(jsonify({'errors': ['Hero or Power not found']}), 404)

        hero_power = HeroPowers(strength=strength, hero_id=hero_id, power_id=power_id)
        
        try:
            db.session.add(hero_power)
            db.session.commit()
        except Exception as e:
            return make_response(jsonify({'errors': ['validation errors']}), 400)

        hero = Hero.query.get(hero_id)
        return make_response(jsonify(hero.to_dict()), 200)

api.add_resource(HeroPowers, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555)
