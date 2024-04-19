from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    created = db.Column(db.String(120))
    #me falta la linea de favoritos con planet


    def __repr__(self):
        return '<User %r>' % self.email  #ponemos el nombre de la variable que existe, no name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "last_name": self.last_name,
            "created": self.created,
            # do not serialize the password, its a security breach
        }
    

class Planet(db.Model):
    __tablename__ = "planet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(80))
    diameter = db.Column(db.Integer)
    gravity = db.Column(db.Integer)
    #favoritos = relationship('FavoritosPlanet', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planet %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
        }


class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    birth_year = db.Column(db.String(80))
    eye_color = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    #favoritos = relationship('FavoritosCharacter', backref='character', lazy=True)

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
        }
    

class Vehicle(db.Model):
    __tablename__ = "vehicle"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(80), nullable= False)
    passenger = db.Column(db.Integer)
    length = db.Column(db.Integer)
    #favoritos = relationship('FavoritosVehicle', backref='vehicle', lazy=True)

    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passenger": self.passenger,
            "length": self.length,
        }


class FavoritosPlanet(db.Model):
    __tablename__ = "favoritos_planet"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))


    def __repr__(self):
        return '<FavoritosPlanet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }


class FavoritosVehicle(db.Model):
    __tablename__ = "favoritos_vehicle"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))


    def __repr__(self):
        return '<FavoritosVehicle %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id_id,
        }   
    



class FavoritosCharacter(db.Model):
    __tablename__ = "favoritos_character"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

    #favoritos = relationship('FavoritosVehicle', backref='vehicle', lazy=True)

    def __repr__(self):
        return '<FavoritosCharacter %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id_id,
        }

