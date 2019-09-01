from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)


# CLI COMMANDS
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database Created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database Killed')


@app.cli.command('db_seed')
def db_seed():
    mercury = Planets(planet_name='Mercury',
                      planet_type='Class D',
                      home_star='Sol',
                      mass=3.258e23,
                      radius=1516,
                      distance=35.96e6)
    venus = Planets(planet_name='Venus',
                    planet_type='Class K',
                    home_star='Sol',
                    mass=4.8658e24,
                    radius=3760,
                    distance=67.24e6)
    earth = Planets(planet_name='Earth',
                    planet_type='Class M',
                    home_star='Sol',
                    mass=5.97e24,
                    radius=3959,
                    distance=92.96e6)
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name="MP",
                     last_name='ME',
                     email='themp731@gmail.com',
                     password='PASSWORD')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded!')


# END CLI COMMANDS


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='This is Super Simple...or is it?')


@app.route('/not_found')
def not_found():
    return jsonify(message='That wasn\'t found'), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + " you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + ", prepare to enter")


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + " you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + ", prepare to enter")


# A GET ONLY
@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planets.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)

# Login Route
@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message="That email already exists"), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User Created Successfully"), 201

@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test is None:
        return jsonify("No existing user")
    else:
        user_to_delete = User.query.filter_by(email=email).first()
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify(message="User with the email: " + email + " has been deleted")



# Database Models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

# End of database models

if __name__ == '__main__':
    app.run()
