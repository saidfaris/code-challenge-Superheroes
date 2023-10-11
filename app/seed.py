from faker import Faker
from app import db,app
from models import Hero, HeroPowers, Power
from random import randint, choice

fake = Faker()

def create_powers(num_powers):
    powers = []
    for _ in range(num_powers):
        power = Power(
            description=fake.sentence()
        )
        powers.append(power)
    return powers

def create_heroes(num_heroes):
    heroes = []
    for _ in range(num_heroes):
        hero = Hero(
            name=fake.name(),
            super_name=fake.unique.first_name()
        )
        heroes.append(hero)
    return heroes

def create_hero_powers(heroes, powers):
    hero_powers = []
    for hero in heroes:
        for power in powers:
            hero_power = HeroPowers(
                strength=choice(["Strong", "Average", "Weak"]),
                hero_id=hero.id,
                power_id=power.id,
            )
            hero_powers.append(hero_power)
    return hero_powers

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        num_powers = 4
        num_heroes = 10
        powers = create_powers(num_powers)
        heroes = create_heroes(num_heroes)

        db.session.add_all(powers)
        db.session.add_all(heroes)
        db.session.commit()

        hero_powers = create_hero_powers(heroes, powers)
        db.session.add_all(hero_powers)
        db.session.commit()

        print("🦸‍♀️ Seeding complete!")