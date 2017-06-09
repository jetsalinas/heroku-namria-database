"""
API for NAMRIA Mobile app database

:Author:    Jose Enrico T. SALINAS
:Version:   06102017
"""

import os
import datetime
import os
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

    def __init__(self, id, name, latitude, longitude, altitude, status):
        self.lightID = id
        self.lightName = name
        self.lightLatitude = latitude
        self.lightLongitude = longitude
        self.lightAltitude = altitude
        self.lightStatus = status

    def __repr__(self):
        return "<Light '{0}','{1}','{2}','{3}','{4}','{5}'".format(
            self.lightID,
            self.lightName,
            self.lightLatitude,
            self.lightLongitude,
            self.lightAltitude,
            self.lightStatus)

class LightSchema(marshmallow.ModelSchema):
    class Meta:
        model = Light


database.create_all()

#########
## APP ##
#########

@app.route("/")
def home():
        return "Hello world!"

if __name__ == "__main__":
    app.run()
