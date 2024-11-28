from flask import *
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from forum import user_create_forum, user_add_reply
from data import admin_retrieve_forum_data
import html
import re
from auth import *
from classes.user import *
from data import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Secret key for sessions and CSRF protection
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XXS and JS from accessing the session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Helps prevent CSRF attacks from other sites

CORS(app, supports_credentials=True, origins=["http://127.0.0.1:3001"])  # Enables CORS for local development

# Email, username, and password regex patterns for validation
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$')  # Email format validation
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]{3,40}$')  # Username validation (3-40 alphanumeric and allowed symbols)
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&_]{8,40}$')  # Password validation (length, letter, digit, special char)

# User registration function
async def user_auth_register(email, password, first_name, last_name):
    email = email.lower()  # Normalize email to lowercase

    if email in users:  # Check if the email is already in use
        abort(400, description="Email already exists")

    if not EMAIL_PATTERN.match(email):  # Validate email format
        abort(400, description="Invalid email format (valid example: username@example.com)")
    
    if not PASSWORD_PATTERN.match(password):  # Validate password format
        abort(400, description="Password must be 8-40 characters, include at least one letter, one number")
    
    if not USERNAME_PATTERN.match(first_name):  # Validate first name format
        abort(400, description="First name must be 3-40 characters, and contain no special characters except . or _ or -")
    
    if not USERNAME_PATTERN.match(last_name):  # Validate last name format
        abort(400, description="Last name must be 3-40 characters, and contain no special characters except . or _ or -")

    # Create and store the new user in the database
    new_user = User(email, first_name, last_name, password)
    users[email] = new_user

    # Generate secure session and CSRF tokens
    return new_user.session_token, new_user.csrf_token 

# Input sanitization to prevent XSS attacks
async def sanitise_input(user_input):
    return re.escape(user_input)  # Escape HTML tags and special characters

# Helper function for token validation (checks if the session is valid)
async def token_validation_helper(session_token):
    user_auth_validate_token(session_token)  # Validates session token
    # Add CSRF Protection in the future

@app.route('/')  # Index route for basic testing
def index():
    return 'Index route'

# API to register a user after validating input
@app.route('/auth/register', methods=['GET', 'POST'])
async def register_user():
    data = request.json  # Extracts the user data from the request body
    email = await sanitise_input(data['email'])  # Sanitizes the email input
    password = await sanitise_input(data['password'])  # Sanitizes the password input
    first_name = await sanitise_input(data['firstName'])  # Sanitizes first name
    last_name = await sanitise_input(data['lastName'])  # Sanitizes last name

    try:
        session_token, csrf_token = await user_auth_register(email, password, first_name, last_name)  # Registers the user

        # Creates the response with a success message
        response = make_response(jsonify({"message": "User registered successfully"}), 201) 
        
        # Sets cookies for session and CSRF tokens
        response.set_cookie("authToken", session_token, samesite="Lax", httponly=True, secure=True)  
        response.set_cookie("csrf_token", csrf_token, samesite="Lax", httponly=True, secure=True)  

        return response  # Returns the response with the cookies set
    
    except Exception as e:  # Handles errors during registration
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 406

# API to login the user and generate session tokens
@app.route('/auth/login', methods=['POST'])
async def login_user():
    data = request.json  # Extracts the data from the frontend request
    email = await sanitise_input(data['email'])  # Sanitizes email input
    password = await sanitise_input(data['password'])  # Sanitizes password input

    try:
        session_token, csrf_token = await user_auth_login(email, password)  # Logs in the user

        # Creates response with success message
        response = make_response(jsonify({"message": "User logged in successfully"}), 200)
        
        # Sets cookies for session and CSRF tokens
        response.set_cookie("authToken", session_token, samesite="Lax", httponly=True, path="/", secure=True)
        response.set_cookie("csrf_token", csrf_token, samesite="Lax", httponly=True, path="/", secure=True)

        return response  # Returns the response with the cookies set

    except Exception as e:  # Handles login errors
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

# API to log out the user and delete session cookies
@app.route('/auth/logout', methods=['DELETE'])
async def logout_user():
    try:
        csrf_token = request.cookies.get("csrf_token")  # Retrieves CSRF token from cookies
        session_token = request.cookies.get("authToken")  # Retrieves session token from cookies

        await user_auth_logout(session_token, csrf_token)  # Logs out the user

        # Creates response to inform user of successful logout
        response = make_response(jsonify({"message": "User logged out successfully"}), 200)
        
        # Deletes the cookies
        response.delete_cookie("authToken")
        response.delete_cookie("csrf_token")

        return response  # Returns the logout response

    except Exception as e:  # Handles errors during logout
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

# API to create a new forum question
@app.route('/forum/new/question', methods=['POST'])
async def create_new_forum():
    data = request.json  # Retrieves data from the frontend
    forum_title = await sanitise_input(data['title'])  # Sanitizes title input
    forum_question = await sanitise_input(data['forumQuestion'])  # Sanitizes forum question input

    session_token = request.cookies.get("authToken")  # Retrieves session token from cookies

    try:
        await user_create_forum(forum_title, forum_question, session_token)  # Creates the new forum post
        return jsonify({"message": "Forum created successfully"}), 201  # Success response
    except Exception as e:
        return jsonify({"error": str(e)}), 401  # Error handling

# API to retrieve all forums (admin access)
@app.route('/forum/retrieve', methods=['GET'])
async def retrieve_all_forums():
    try:
        forum_dict = await admin_retrieve_forum_data()  # Retrieves forum data
        return jsonify({"message": "All forum data returned successfully", "forums": forum_dict}), 201  # Success response
    except Exception as e:
        return jsonify({"error": str(e)}), 401  # Error handling

# API to validate session and CSRF tokens
@app.route('/auth/validate', methods=['GET', 'POST'])
async def validate_token():
    session_token = request.cookies.get("authToken")  # Retrieves session token
    csrf_token = request.cookies.get("csrf_token")  # Retrieves CSRF token

    validate_var, error_info = await user_auth_validate_token(session_token, csrf_token)  # Validates tokens

    try:
        if validate_var:
            return jsonify({"message": "Token & CSRF are valid"}), 200  # If valid, return success
        else:
            # Handles errors based on validation failure
            if error_info == "CSRF":
                return jsonify({"error": "Invalid CSRF Token"}), 401
            elif error_info == "Session":
                return jsonify({"error": "Invalid Session Token"}), 401
            else:
                return jsonify({"error": "Unknown validation error"}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500  # General error handling

# API to add a reply to a forum post
@app.route('/forum/reply/submit', methods=['POST'])
async def store_reply():
    data = request.json  # Retrieves reply data
    forum_id = await sanitise_input(str(data['forumId']))  # Sanitizes forum ID
    reply_comment = await sanitise_input(data['reply'])  # Sanitizes reply comment

    session_token = request.cookies.get("authToken")  # Retrieves session token

    try:
        await user_add_reply(forum_id, reply_comment, session_token)  # Adds reply to the forum post
        return jsonify({"message": "Forum reply added successfully"}), 201  # Success response
    except Exception as e:
        return jsonify({"error": str(e)}), 401  # Error handling

if __name__ == '__main__':
    app.run(debug=False, port=5005)
