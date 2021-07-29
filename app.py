import numpy as np

import sqlalchemy
from sqlalchemy.sql import select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, request, render_template, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
# station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date,measurement.prcp).all()
    session.close()

    precipitation_data =[]

    for date, prcp in results:
        measurement_dict = {}
        measurement[0] = date
        measurement[1] = precipitation
        precipitation_data.append(measurement_dict)
    
    return jsonify (precipitation_data)





if __name__ == "__main__":
    app.run(debug=True)
