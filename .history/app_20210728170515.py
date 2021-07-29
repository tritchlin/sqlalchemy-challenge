from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import climate_flask_data.py as querydata

app = Flask(__name__)
app.config['Hawaii']='sqlite:///hawaii.sqlite'
db=SQLAlchemy(app)

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = base.classes.measurement
station = base.classes.station

# Define what to do when a user hits the index route
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

# Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # return querydata.precipitation()
    return "<p>Hello, World!</p>"

# # Define what to do when a user hits the /about route
# @app.route("/api/v1.0/stations")
# def about():
#     print("Server received request for 'About' page...")
#     return "Welcome to my 'About' page!"

# # Define what to do when a user hits the /about route
# @app.route("/api/v1.0/tobs")
# def about():
#     print("Server received request for 'About' page...")
#     return "Welcome to my 'About' page!"

# # Define what to do when a user hits the /about route
# @app.route("/api/v1.0/<start>")
# def about():
#     print("Server received request for 'About' page...")
#     return "Welcome to my 'About' page!"

# # Define what to do when a user hits the /about route
# @app.route("/api/v1.0/<start>/<end>")
# def about():
#     print("Server received request for 'About' page...")
#     return "Welcome to my 'About' page!"

# if __name__ == "__main__":
#     app.run(debug=True)
