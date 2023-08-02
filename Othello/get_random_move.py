from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/get_random_move', methods=['POST'])
def get_random_move():
    board_state = request.json['board_state']
    
    # Generate a random move (row, col) here
    random_move = (random.randint(0, 7), random.randint(0, 7))
    
    return jsonify({'random_move': random_move})

if __name__ == '__main__':
    app.run()