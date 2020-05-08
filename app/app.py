from redis import Redis
import os
from flask import Flask, jsonify

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
REDIS_HOST = os.environ.get('REDIS_HOST')
redis_client = Redis(host=REDIS_HOST)
print(REDIS_HOST)


def caching(function):
    def wrap(number):
        stored_value = redis_client.get(number)
        if stored_value:
            return int(stored_value.decode())
        new_value = function(number)
        redis_client.set(number, new_value)
        return new_value
    return wrap


@caching
def get_fibonacci(number):
    if (number == 0) or (number == 1): 
        return number
    return get_fibonacci(number-1) + get_fibonacci(number-2)


@app.route('/')
def hello_world1():
    return 'Hello, Docker!'


@app.route("/<number>", methods=['GET'])
def hello_world(number):
    number = int(number)
    stored_value = redis_client.get(number)
    if stored_value:
        return jsonify({number: stored_value.decode()}), 200
    new_value = get_fibonacci(number)
    redis_client.set(number, new_value)
    return jsonify({number: new_value}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
