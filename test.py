from flask import Flask, request, jsonify 
from flasgger import Swagger
from datetime import datetime, timedelta
import time

app = Flask(__name__)
app.config['SWAGGER'] = {
    "title": "My API",
    "description": "My API",
    "version": "1.0.2",
    "termsOfService": "",
    "hide_top_bar": True
}

Swagger(app)

# Simulated database for storing accounts
accounts = {}
MAX_ATTEMPTS = 5
WAIT_TIME = timedelta(minutes=1)
verification_attempts = {}
error_time = 0  # global variable

@app.route('/')
def hello():
    return 'Hello, World! backend in running'

# Error handler
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request", "message": error.description}), 400


@app.route("/create_account", methods=["POST"])
def create_account():
    """
    This endpoint creates a new user account.
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: The username of the new account.
      - name: password
        in: formData
        type: string
        required: true
        description: The password of the new account.
    responses:
      200:
        description: Success response
        schema:
          properties:
            success:
              type: boolean
              description: Indicates whether the account creation was successful.
            message:
              type: string
              description: A message indicating the result of the account creation.
      400:
        description: Bad request response
        schema:
          properties:
            error:
              type: string
              description: Error message indicating the reason for the bad request.
            message:
              type: string
              description: A message indicating the result of the account creation.
    """
    # Parse JSON payload

    username = request.values["username"]
    password = request.values["password"]
    print(password, username)

    # Check if username already exists
    if username in accounts:
        return jsonify({"success": False, "reason": "Username already exists"})

    # Validate username and password
    if len(username) < 3 or len(username) > 32:
        return jsonify(
            {
                "success": False,
                "reason": "Username length should be between 3 and 32 characters",
            }
        )
    if len(password) < 8 or len(password) > 32:
        return jsonify(
            {
                "success": False,
                "reason": "Password length should be between 8 and 32 characters",
            }
        )
    if not any(char.isupper() for char in password):
        return jsonify(
            {
                "success": False,
                "reason": "Password should contain at least one uppercase letter",
            }
        )
    if not any(char.islower() for char in password):
        return jsonify(
            {
                "success": False,
                "reason": "Password should contain at least one lowercase letter",
            }
        )
    if not any(char.isdigit() for char in password):
        return jsonify(
            {"success": False, "reason": "Password should contain at least one digit"}
        )

    # Create account
    accounts[username] = password
    return jsonify({"success": True})


@app.route("/verify_account", methods=["POST"])
def verify_account():
    """
    This endpoint verifies the user account.
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: The username of the account to be verified.
      - name: password
        in: formData
        type: string
        required: true
        description: The password of the account to be verified.
    responses:
      200:
        description: Success response
        schema:
          properties:
            success:
              type: boolean
              description: Indicates whether the account verification was successful.
            message:
              type: string
              description: A message indicating the result of the account verification.
      400:
        description: Bad request response
        schema:
          properties:
            error:
              type: string
              description: Error message indicating the reason for the bad request.
            message:
              type: string
              description: A message indicating the result of the account verification.
      429:
        description: Too many failed attempts response
        schema:
          properties:
            message:
              type: string
              description: A message indicating that there are too many failed attempts.
    """
    # Parse JSON payload
    global error_time

    username = request.values["username"]
    password = request.values["password"]
    print(accounts)

    if error_time >= MAX_ATTEMPTS:
        time.sleep(5)
        error_time = 0
    # Check if username exists
    if username not in accounts:
        error_time += 1
        if error_time >= MAX_ATTEMPTS:
            return (
                jsonify(
                    {
                        "message": "Too many failed attempts. Please try again later and wait for one minutes."
                    }
                ),
                429,
            )

        return jsonify({"success": False, "reason": "Username does not exist"})

    # Verify password
    if accounts[username] == password:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "reason": "Incorrect password"})


if __name__ == "__main__":
    app.run(debug=True)
