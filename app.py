from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/super_simple')
def super_simple():
    return jsonify(message='This is Super Simple...or is it?')

@app.route('/not_found')
def not_found():
    return jsonify(message='That wasn\'t found'), 404


@app.route('/parameters')
def parameters():
    name = ''
    age = 0


if __name__ == '__main__':
    app.run()
