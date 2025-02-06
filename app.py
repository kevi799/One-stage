from flask import Flask, request, Response
import json
import requests
import math
from flask_cors import CORS
from flask_caching import Cache
from collections import OrderedDict

app = Flask(__name__)
CORS(app)

app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    if n < 2:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n):
    digits = [int(d) for d in str(abs(n))]
    num_digits = len(digits)
    return sum(d ** num_digits for d in digits) == abs(n)

def digit_sum(n):
    return sum(int(d) for d in str(abs(n)))

@cache.memoize(timeout=3600)
def get_fun_fact(n, properties):
    if "armstrong" in properties:
        digits = [int(d) for d in str(abs(n))]
        num_digits = len(digits)
        armstrong_calc = " + ".join(f"{d}^{num_digits}" for d in digits)
        return f"{n} is an Armstrong number because {armstrong_calc} = {n}"

    url = f"http://numbersapi.com/{abs(n)}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return "No fun fact available."

def generate_error_response(number):
    error_response = OrderedDict([
        ("error", True)
    ])
    return Response(json.dumps(error_response, sort_keys=False), mimetype='application/json'), 400

@app.route('/')
def home():
    return Response(json.dumps({
        "message": "Welcome to the Number Classification API! Use /api/classify-number?number=<your_number>"
    }), mimetype='application/json'), 200

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    if not number:
        return generate_error_response(number)

    if not number.lstrip('-').isdigit():
        return generate_error_response(number)

    number = int(number)

    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    properties.append("even" if number % 2 == 0 else "odd")

    result = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_perfect(number),
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number, properties)
    }

    ordered_response = OrderedDict([
        ("number", result["number"]),
        ("is_prime", result["is_prime"]),
        ("is_perfect", result["is_perfect"]),
        ("properties", result["properties"]),
        ("digit_sum", result["digit_sum"]),
        ("fun_fact", result["fun_fact"])
    ])

    return Response(json.dumps(ordered_response, sort_keys=False), mimetype='application/json'), 200

if __name__ == '__main__':
    app.run(debug=True)
