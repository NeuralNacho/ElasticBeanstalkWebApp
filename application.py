from flask import Flask, request, jsonify
# from flask_cors import CORS
import random

application = Flask(__name__)
# CORS(application)  # Enable CORS for all routes. 
# i.e. live server will have permission to talk to this server

@application.route('/')
def index():
    # This method will display the static page (html, css, js)
    return application.send_static_file('index.html')

@application.route('/get_random_move', methods=['POST'])
def get_random_move():
    if request.method == 'POST':
        # Generate a random move here
        random_move = [random.randint(0, 7), random.randint(0, 7)]
        return jsonify({"random_move": random_move})
    else:
        return jsonify({"error": "Invalid request method"})

if __name__ == '__main__':
    application.run(debug=True)

# To do with separate flask server and webpage, don't need the index function
# but will need to be carful with enabling ports etc.

# EC-2 notes: For the service role for some reason it shows the instance profile
# as a role but this won't work. Also don't use existing service role but rather 
# aws-elasticbeanstalk-service-role under create service role.
# Then for instance profile set up the role on IAM as desribed by the documentation.