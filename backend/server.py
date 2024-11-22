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
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XXS and JS 
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Helps prevent CSRF attacks from different sites

CORS(app, supports_credentials=True, origins=["http://127.0.0.1:3001"])

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$') # Email pattern: typical email structure
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.-]{3,40}$') # Username pattern: Ensures names have 3-20 alphanumeric characters and some symbols
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,40}$') # Password pattern: Enforces length, letter, digit, and special character requirements, while must also be between 8 & 20 characters long

# User registration function
async def user_auth_register(email, password, first_name, last_name):
    email = email.lower()  # Normalize email to lowercase

    if email in users:
        abort(400, description="Email already exists")

    if not EMAIL_PATTERN.match(email):
        abort(400, description="Invalid email format (valid example: username@example.com)")
    
    if not PASSWORD_PATTERN.match(password):
        abort(400, description="Password must be 3-40 characters, include at least one letter, one number, and one special character")
    
    if not USERNAME_PATTERN.match(first_name):
        abort(400, description="First name must be 3-40 characters, and contain no special characters except . or _ or -")
    
    if not USERNAME_PATTERN.match(last_name):
        abort(400, description="Last name must be 8-40 characters, and contain no special characters except . or _ or -")

    # Create and store the new user
    new_user = User(email, first_name, last_name, password)
    users[email] = new_user

    # Generate secure session and CSRF tokens
    return new_user.session_token, new_user.csrf_token 


#XSS Sanitation
async def sanitise_input(user_input):
    # Basic HTML escaping
    return html.escape(user_input)

#Helper Token Validation Fuction
async def token_validation_helper(session_token):
    user_auth_validate_token(session_token)
    #Add CSRF Protection

"""
EXCLUDED_ROUTES = ['/', '/auth/register', '/auth/login', '/auth/logout']

@app.before_request
def csrf_validation():
    if request.endpoint in EXCLUDED_ROUTES:
        return
"""

@app.route('/') 
def index():
    return 'Index route'

# POST API to register a user

@app.route('/auth/register', methods=['GET','POST']) #Creates the User
async def register_user():
    data = request.json
    email = await sanitise_input(data['email'])
    password = await sanitise_input(data['password'])
    first_name = await sanitise_input(data['firstName'])
    last_name = await sanitise_input(data['lastName'])

    try:
        session_token, csrf_token = await user_auth_register(email, password, first_name, last_name)                       

        print(session_token, csrf_token)

        response = make_response(jsonify({"message": "User registered successfully"}), 201)
        
        response.set_cookie("authToken", session_token, samesite="Lax", httponly=True, secure=True)
        response.set_cookie("csrf_token", csrf_token, samesite="Lax", httponly=True, secure=True)

        return response
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 406

@app.route('/auth/login', methods=['POST']) #Logins the User, giving them a session token
async def login_user(): 
    data = request.json
    email = await sanitise_input(data['email'])
    password = await sanitise_input(data['password'])

    print(password)

    try:

        session_token, csrf_token = await user_auth_login(email, password)                     

        response = make_response(jsonify({"message": "User registered successfully"}), 201)
        response.set_cookie("authToken", session_token, samesite="Lax", httponly=True, path = "/", secure=True)
        response.set_cookie("csrf_token", csrf_token, samesite="Lax", httponly=True, path = "/", secure=True)

        return response
                  
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

@app.route('/auth/logout', methods=['DELETE'])                                                                  
async def logout_user():

    try:

        csrf_token = request.cookies.get("csrf_token")
        session_token = request.cookies.get("authToken")

        await user_auth_logout(session_token, csrf_token)

        response = make_response(jsonify({"message": "User logged out successfully"}), 200)
        response.delete_cookie("authToken")
        response.delete_cookie("csrf_token")

        return response

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

    
@app.route('/forum/new/question', methods=['POST']) 
async def create_new_forum():
    data = request.json
    forum_title = await sanitise_input(data['title'])
    forum_question = await sanitise_input(data['forumQuestion'])

    session_token = request.cookies.get("authToken")

    try:
        await user_create_forum(forum_title, forum_question, session_token)
        return jsonify({"message": "Forum created succesfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    
@app.route('/forum/retrieve', methods=['GET']) 
async def retrieve_all_forums():

    try:
        forum_dict = await admin_retrieve_forum_data()
        return jsonify({"message": "All forum data returned succesfully", "forums": forum_dict}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/auth/validate', methods=['GET','POST'])                            
async def validate_token():

    session_token = request.cookies.get("authToken")
    csrf_token = request.cookies.get("csrf_token")

    validate_var, error_info = await user_auth_validate_token(session_token, csrf_token)               

    try:
        if validate_var:                                               
                return jsonify({"message": "Token & CSRF is valid"}), 200
        else:                                                                        
                if error_info == "CSRF":
                    return jsonify({"error": "Invalid CSRF Token"}), 401
                elif error_info == "Session":
                    return jsonify({"error": "Invalid Session Token"}), 401
                else:
                    return jsonify({"error": "Unknown validation error"}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500
        
@app.route('/forum/reply/submit', methods=['POST'])
async def store_reply():
    data = request.jsond
    forum_id = await sanitise_input(str(data['forumId']))
    reply_comment = await sanitise_input(data['reply'])

    session_token = request.cookies.get("authToken")

    try:
        await user_add_reply(forum_id, reply_comment, session_token)
        return jsonify({"message": "Forum reply added succesfully"}), 201
    except Exception as e:
        
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5005)
