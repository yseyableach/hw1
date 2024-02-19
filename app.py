from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulated database for storing accounts
accounts = {}

# Error handler
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': error.description}), 400


@app.route('/create_account', methods=['POST'])
def create_account():
    # Parse JSON payload

    username = request.values['username']
    password = request.values['password']
    print(password,username)
    
    # Check if username already exists
    if username in accounts:
        return jsonify({'success': False, 'reason': 'Username already exists'})

    # Validate username and password
    if len(username) < 3 or len(username) > 32:
        return jsonify({'success': False, 'reason': 'Username length should be between 3 and 32 characters'})
    if len(password) < 8 or len(password) > 32:
        return jsonify({'success': False, 'reason': 'Password length should be between 8 and 32 characters'})
    if not any(char.isupper() for char in password):
        return jsonify({'success': False, 'reason': 'Password should contain at least one uppercase letter'})
    if not any(char.islower() for char in password):
        return jsonify({'success': False, 'reason': 'Password should contain at least one lowercase letter'})
    if not any(char.isdigit() for char in password):
        return jsonify({'success': False, 'reason': 'Password should contain at least one digit'})

    # Create account
    accounts[username] = password
    return jsonify({'success': True})


@app.route('/verify_account', methods=['POST'])
def verify_account():
    # Parse JSON payload
    username = request.values['username']
    password = request.values['password']
    print(accounts)

    # Check if username exists
    if username not in accounts:
        return jsonify({'success': False, 'reason': 'Username does not exist'})

    # Verify password
    if accounts[username] == password:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'reason': 'Incorrect password'})


if __name__ == '__main__':
    app.run(debug=True)
