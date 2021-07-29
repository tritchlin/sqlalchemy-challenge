from flask import Flask

#  Create an app, being sure to pass __name__
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"

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
@app.route("/api/v1.0/precipitation")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

if __name__ == "__main__":
    app.run(debug=True)
