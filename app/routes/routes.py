from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

#Create a new Planet
@planets_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    new_planet = Planet(name=request_body["name"],
                    description=request_body["description"],
                    revolution_period=request_body["revolution_period"]
                    )

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} successfully created", 201)

@planets_bp.route("", methods=["GET"])
def read_all_planets():
    planets_response = []
    planets = Planet.query.all()
    for planet in planets:
        planets_response.append(
            {
                "id": planet.id,
                "name": planet.name,
                "description": planet.description,
                "revolution_period": planet.revolution_period
            }
        )
    return jsonify(planets_response)

#Error Handling an invalid planet or non-existing planet
def validate_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message":f"planet {planet_id} invalid"}, 400))

    planet = planet.query.get(planet_id)

    if not planet:
        abort(make_response({"message":f"planet {planet_id} not found"}, 404))

    return planet

#Get a Single(specific) planet endpoint
@planets_bp.route("/<planet_id>", methods=["GET"])
def read_one_planet(planet_id):
    planet = validate_planet(planet_id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "revolution_period": planet.revolution_period
    }

# class Planet:
#     def __init__(self, id, name, description, revolution_period):
#        self.id = id
#        self.name = name 
#        self.description = description
#        self.revolution_period = revolution_period

# PLANETS = [
#     Planet(1, "Mercury", "terrestrial", "87.97 days"),
#     Planet(2, "Venus", "terrestrial", "224.7 days"),
#     Planet(3, "Earth", "terrestrial", "365.26 days"),
#     Planet(4, "Mars", "terrestrial", "1.88 years"),
#     Planet(5, "Jupiter", "gaseous", "11.86 years"),
#     Planet(6, "Saturn", "gaseous", "29.46 years"),
#     Planet(7, "Uranus", "gaseous", "84.01 years"),
#     Planet(8, "Neptune", "gaseous", "164.79 years"),
#     Planet(9, "Pluto", "icy, rocky", "248.59 years")
# ]
