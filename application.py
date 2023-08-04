from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes. 
# i.e. live server will have permission to talk to this server

@app.route('/')
def index():
    # This method will display the static page (html, css, js)
    return app.send_static_file('index.html')

@app.route('/get_random_move', methods=['POST'])
def get_random_move():
    if request.method == 'POST':
        # Generate a random move here
        random_move = [random.randint(0, 7), random.randint(0, 7)]
        return jsonify({"random_move": random_move})
    else:
        return jsonify({"error": "Invalid request method"})

if __name__ == '__main__':
    app.run(debug=True)

# To do with separate flask server and webpage, don't need the index function
# but will need to be carful with enabling ports etc.


# To do the same think with everything on the same server do the following:
# (This is the way it is currently)
# Change the project structure:
# project_folder/
# ├── static/
# │   ├── index.html
# ├── app.py
# Add the following function to the Python app:
# @app.route('/')
# def index():
#     # This method will display the static page (html, css, js)
#     return app.send_static_file('othello.html')
# Lastly, change the href's in the html file to e.g. /static/othello.css