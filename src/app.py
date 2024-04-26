"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, FavoritosCharacter, FavoritosPlanet,FavoritosVehicle    #IMPORTAR TABLAS AQUI
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
 

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



#ENDPOINTS A PARTIR DE AQUI


@app.route('/signup', methods=['POST'])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_query = User.query.filter_by(email=email).first()
    if user_query is None:
        new_user = User(email= email, password= password)
        db.session.add(new_user)
        db.session.commit()
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "the user already exists "}), 401


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user_query = User.query.filter_by(email=email).first()

    if user_query is None:
        return jsonify({"msg": "email doesn't exist"}), 404
    
    if email != user_query.email or password != user_query.password:
        return jsonify({"msg": "wrong email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)



@app.route('/users', methods=['GET'])  #ENDPOINT para obtener allUsers
def get_all_users():
        #aqui llamo a mi tabla, que esta en models.py
    query_results = User.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
    if results == []:
         return jsonify({"msg": "user not found"}), 404
    response_body = {
        "msg": "ok",
        "results": results
    }
    return jsonify(response_body), 200


@app.route('/users/favorites', methods=['GET'])  #ENDPOINT para obtener listado de favoritos que pertenecen al user actual
@jwt_required()
def get_list_favorites():
    email = get_jwt_identity()
    user_query = User.query.filter_by(email=email).first()
    user_id=user_query.id

    favorite_character = FavoritosCharacter.query.filter_by(user_id=user_id).all()
    favorite_planet = FavoritosPlanet. query.filter_by(user_id=user_id).all()
    favorite_vehicle = FavoritosVehicle.query.filter_by(user_id=user_id).all()
    results_character = list(map(lambda item: item.serialize(), favorite_character))
    results_planet = list(map(lambda item: item.serialize(), favorite_planet))
    results_vehicle = list(map(lambda item: item.serialize(), favorite_vehicle))
    
    if results_character == [] and results_planet == [] and results_vehicle == []:
        return jsonify({"msg": "favorites not found"}), 404
    response_body = {
        "msg": "ok",
        "results": [results_character, results_planet, results_vehicle],
        }
    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])  #ENDPOINT para obtener allPeople
def get_all_people():
    query_results = Character.query.all()
    results = list(map(lambda item: item.serialize(), query_results)) #mapeo porque se trata de un array
    if results == []:
         return jsonify({"msg": "character not found"}), 404
    response_body = {
        "msg": "ok",
        "results": results
    }
    return jsonify(response_body), 200



@app.route('/people/<int:people_id>', methods=['GET'])  #ENDPOINT para obtener info de un personaje segun su id
def get_one_people(people_id):
    people_query = Character.query.filter_by(id=people_id).first()
    # query_results = Character.query.all()
    if people_query is None:
          return jsonify({"msg": "character not found"}), 404
    response_body = {
        "msg": "ok",
        "results": people_query.serialize()
    }
    return jsonify(response_body), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])   #ENDPOINT para eliminar un character favorito con el id
def delete_people(people_id):
    people_deleted = Character.query.filter_by(id=people_id).first()
    if people_deleted:
        db.session.delete(people_deleted)
        db.session.commit()
        return jsonify({"msg": "character was successfully deleted"}), 200
    else:
        return jsonify({"msg": "character not found"}), 404 


@app.route('/planets', methods=['GET'])  #ENDPOINT para listar todos los registros de planets en la db
def get_all_planet():
    #aqui llamo a mi tabla, que esta en models.py
    query_results = Planet.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
    if results == []:
         return jsonify({"msg": "planet not found"}), 404
    response_body = {
        "msg": "ok",
        "results": results
    }
    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])  #ENDPOINT para obtener info de un planeta concreto
def get_one_planet(planet_id):
    planet_query = Planet.query.filter_by(id=planet_id).first()
    # query_results = Character.query.all()
    if planet_query is None:
          return jsonify({"msg": "planet not found"}), 404
    response_body = {
        "msg": "ok",
        "results": planet_query.serialize()
    }
    return jsonify(response_body), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])   #ENDPOINT para eliminar un planet favorito con el id
def delete_planet(planet_id):
    planet_deleted = Planet.query.filter_by(id=planet_id).first()
    if planet_deleted:
        db.session.delete(planet_deleted)
        db.session.commit()
        return jsonify({"msg": "planet was successfully deleted"}), 200
    else:
        return jsonify({"msg": "planet not found"}), 404 


@app.route('/vehicle', methods=['GET'])  #ENDPOINT para obtener allVehicles
def get_all_vehicle():
    query_results = Vehicle.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
    if results == []:
         return jsonify({"msg": "vehicle not found"}), 404
    response_body = {
        "msg": "ok",
        "results": results
    }
    return jsonify(response_body), 200


@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])  #ENDPOINT para obtener un vehículo
def get_one_vehicle(vehicle_id):
    vehicle_query = Vehicle.query.filter_by(id=vehicle_id).first()
    if vehicle_query is None:
          return jsonify({"msg": "vehicle not found"}), 404
    response_body = {
        "msg": "ok",
        "results": vehicle_query.serialize()
    }
    return jsonify(response_body), 200


@app.route('/people', methods=['POST'])  #ENDPOINT para CREAR personaje
def create_people():
    body = request.json
    people_query = Character.query.filter_by(name=body["name"]).first()
    if people_query is None:
        new_people = Character(name= body["name"], birth_year= body["birth_year"], eye_color=body ["eye_color"], gender=body["gender"])
        db.session.add(new_people)
        db.session.commit()
        return jsonify({"msg": "character created"}), 200
    else:
        return jsonify({"msg": "character exist"}), 404



@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])  #ENDPOINT para AÑADIR un planet fav al usuario actual
@jwt_required() #aun tengo que trabajar en el token de autenticación
def add_fav_planet_to_user():
    email = get_jwt_identity()
    query_results = User.query.filter_by(email=email).first()
    user_id = query_results.id
    planet_query = Planet.query.filter_by(id="planet_id").first()
    if planet_query is None:
        return ({"msg": "this planet doesn't exist"}), 400
    else:
        favorite_planet_exist = FavoritosPlanet.query.filter_by(planet_id="planet_id", user_id=user_id).first()
        if favorite_planet_exist is None:
            new_favorite_planet = FavoritosPlanet(planet_id="planet_id", user_id=user_id).first()
            db.session.add(new_favorite_planet)
            db.session.commit()
            return jsonify({"msg": "planet added"}), 200
        else:
            return jsonify({"msg": "planet already exist"}), 404



@app.route('/favorite/people/<int:people_id>', methods=['POST'])  #ENDPOINT para AÑADIR un character fav al usuario actual
def add_fav_character_to_user():
    body = request.json
    favorite_character_query = FavoritosCharacter.query.filter_by(user_id=body["user_id"]).first()
    if favorite_character_query is None:
        new_favorite_character = FavoritosCharacter(user_id= body["user_id"], character_id= body["character_id"])
        db.session.add(new_favorite_character)
        db.session.commit()
        return jsonify({"msg": "character added"}), 200
    else:
        return jsonify({"msg": "character exist"}), 404
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
