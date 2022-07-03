from flask import Flask, Blueprint


rand = Blueprint('random', __name__)


@rand.route('/hi', methods=['GET'])
def index():
    return 'Hello, World!'
