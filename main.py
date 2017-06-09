"""
API for NAMRIA Mobile app database

:Author:    Jose Enrico T. SALINAS
:Version:   06102017
"""

import os
import datetime
import csv
import re

from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
from flask_cors import CORS, cross_origin

from flask import Flask
app = Flask(__name__)
CORS(app)
database = SQLAlchemy(app)
marshmallow = Marshmallow(app)

#############
## SCHEMA  ##
#############

class Light(database.Model):
    __tablename__ = "lights"

    lightID = database.Column(database.Integer, primary_key=True)
    lightName = database.Column(database.String)
    lightLatitude = database.Column(database.Float)
    lightLongitude = database.Column(database.Float)
    lightAltitude = database.Column(database.Float)
    lightStatus = database.Column(database.Boolean)

    """
    def __init__(self, id, name, latitude, longitude, altitude, status):
        self.lightID = id
        self.lightName = name
        self.lightLatitude = latitude
        self.lightLongitude = longitude
        self.lightAltitude = altitude
        self.lightStatus = status
    """

    def __repr__(self):
        return "Light '{0}','{1}','{2}','{3}','{4}','{5}'".format(
            self.lightID,
            self.lightName,
            self.lightLatitude,
            self.lightLongitude,
            self.lightAltitude,
            self.lightStatus)

class LightSchema(marshmallow.ModelSchema):
    class Meta:
        model = Light

lights = []
with open("listoflights.csv") as lights_csv:
    lights_list = csv.reader(lights_csv)
    for row in lights_list:
        lights.append(Light(
            lightID=row[0],
            lightName=row[1],
            lightLatitude=row[2],
            lightLongitude=row[3],
            lightAltitude=row[4],
            lightStatus=row[5]
            ))

for light in lights:
    print(light.__repr__())

"""
test = Light(
    lightID=322,
    lightName="John Kinsey",
    lightLatitude=122.32112,
    lightLongitude=4.213213,
    lightAltitude=30,
    lightStatus=True
    )

print(test.lightID)
print(test.lightName)
print(test.lightLatitude)
print(test.lightLongitude)
print(test.lightAltitude)
print(test.lightStatus)
"""

#########
## APP ##
#########

@app.route("/")
def home():
        return "Hello world!"

if __name__ == "__main__":
    app.run()
