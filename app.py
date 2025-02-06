from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import math

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def get_homepage():
    return jsonify({"message": "Welcome"}), 200

@app.route('/api/classify-number', methods=['GET'])
def get_funfact():
    number = request.args.get('number', None)
    try:
        if number is None or not number.lstrip('-').isdigit():
            return jsonify({"number": f"{number}", "error": True}), 400

        number = int(number)

        result = {
            "number": number,
            "is_prime": False,
            "is_perfect": False, 
            "properties": [],
            "digit_sum": sum(int(digit) for digit in str(abs(number))),
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

        return jsonify(result)

    except Exception as err:
        return jsonify({"error": f"An error occurred: {str(err)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
