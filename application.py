from flask import Flask
from backend.Othello.get_othello_move import othello_blueprint
# from flask_cors import CORS

application = Flask(__name__)
# CORS(application)  # Enable CORS for all routes. 
# i.e. live server will have permission to talk to this server
application.register_blueprint(othello_blueprint)

@application.route('/')
def index():
    # This method will display the static page (html, css, js)
    return application.send_static_file('index.html')

if __name__ == '__main__':
    application.run(debug = True)

# To do with separate flask server and webpage, don't need the index function
# but will need to be carful with enabling ports etc.

# EC-2 notes: For the service role for some reason it shows the instance profile
# as a role but this won't work. Also don't use existing service role but rather 
# aws-elasticbeanstalk-service-role under create service role.
# Then for instance profile set up the role on IAM as desribed by the documentation.

# HTTPS notes: get SSL certificate but setting up certbot on EC2 instance.
# Done by following certbot installation instructions for NGINX an PIP. (use dnf instead of apt)
# ssh into server by running ssh -i pipelined-portfolio-key-pair.pem ec2-user@18.170.241.179
# from command line