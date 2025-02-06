from flask import Flask, request, Response
import json
import requests
import math
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

def generate_error_response():
    error_response = {
        "error": True
    }
    return Response(json.dumps(error_response), mimetype='application/json'), 400

@app.route('/')
def home():
    return Response(json.dumps({"message": "Welcome"}), mimetype='application/json'), 200

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    if not number or not number.lstrip('-').isdigit():
        return generate_error_response()

    number = int(number)

    result = {
        "number": number,
        "is_prime": False,
        "is_perfect": False,
        "properties": [],
        "digit_sum": digit_sum(number),
        "fun_fact": None
    }

    if number > 1:
        if number == 2 or number == 3:
            result["is_prime"] = True
        elif number % 2 == 0 or number % 3 == 0:
            result["is_prime"] = False
        else:
            for i in range(5, int(math.sqrt(number)) + 1, 2):
                if number % i == 0:
                    result["is_prime"] = False
                    break
            else:
                result["is_prime"] = True

    if number % 2 == 0:
        result["properties"].append("even")
    else:
        result["properties"].append("odd")

    num_digits = len(str(abs(number)))
    sum_of_powers = sum(int(digit) ** num_digits for digit in str(abs(number)))
    if sum_of_powers == abs(number):
        result["properties"].append("armstrong")

    if number > 1:
        perfect_sum = 1
        for i in range(2, int(math.sqrt(number)) + 1):
            if number % i == 0:
                perfect_sum += i
                if i != number // i:
                    perfect_sum += number // i
        result["is_perfect"] = (perfect_sum == number)

    if number >= 0:
        response = requests.get(f"http://numbersapi.com/{number}")
        result["fun_fact"] = response.text if response.status_code == 200 else "No fun fact available."
    else:
        result["fun_fact"] = "Fun facts are only available for positive numbers."

    return Response(json.dumps(result, sort_keys=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
