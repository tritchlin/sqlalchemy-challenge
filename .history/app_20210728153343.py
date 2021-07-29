from flask import Flask

#  Create an app, being sure to pass __name__
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"

# Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# Define what to do when a user hits the /about route
@app.route("/api/v1.0/stations")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# Define what to do when a user hits the /about route
@app.route("/api/v1.0/tobs")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# Define what to do when a user hits the /about route
@app.route("/api/v1.0/<start>")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# Define what to do when a user hits the /about route
@app.route("/api/v1.0/<start>/<end>")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

if __name__ == "__main__":
    app.run(debug=True)
