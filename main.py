"""
API for NAMRIA Mobile app database

:Author:    Jose Enrico T. SALINAS
:Version:   06102017
:Notes: Adapted from github.com/blubits/streserve by Maded Batara III
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

if 'DYNO' in os.environ:
    import psycopg2
    hr = Heroku(app)
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'

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

#CLEARS DATABASE FROM FRESH RUN
if 'DYNO' not in os.environ:
    database.reflect()
    database.drop_all()

#LOAD DATABASE FROM CSV FILE
database.create_all()
for light in lights:
    database.session.add(light)
database.session.commit()

#LOAD SCHEMAS
light_schema = LightSchema()

#########
## APP ##
#########

@app.route("/")
def home():
        return "Hello world!"

@app.route("/lights")
def get_all_lights():
    result = [
        light_schema.dump(light).data
        for light in Light.query.all()
    ]
    return jsonify(result)

if __name__ == "__main__":
    app.run()
