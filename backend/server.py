from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from auth import user_auth_register, user_auth_login, user_auth_logout, user_auth_validate_token
from forum import user_create_forum, user_add_reply
from data import admin_retrieve_forum_data
import html

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XXS and JS 
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Helps prevent CSRF attacks from different sites

CORS(app)

#XSS Sanitation
def sanitise_input(user_input):
    # Basic HTML escaping
    return html.escape(user_input)

#Helper Token Validation Fuction
def token_validation_helper(session_token):
    user_auth_validate_token(session_token)
    #Add CSRF Protection

@app.route('/') 
def index():
    return 'Index route'

# POST API to register a user

@app.route('/auth/register', methods=['POST']) #Creates the User
def register_user():
    data = request.json
    email = sanitise_input(data['email'])
    password = sanitise_input(data['password'])
    first_name = sanitise_input(data['firstName'])
    last_name = sanitise_input(data['lastName'])

    try:
        session_token, csrf_token = user_auth_register(email, password, first_name, last_name)                      #Authentication Register - Stage 1.2 || Stage 2.1 & 2.2 Returns csrf_token & session token
        return jsonify({"message": "User registered successfully", "token": session_token, "csrf_token": csrf_token}), 201
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 406

@app.route('/auth/login', methods=['POST']) #Logins the User, giving them a session token
def login_user(): 
    data = request.json
    email = sanitise_input(data['email'])
    password = sanitise_input(data['password'])

    try:
        session_token, csrf_token = user_auth_login(email, password)                                                #Stage 2.1 & 2.2 Returns logged User's csrf_token & session token
        return jsonify({"message": "User logged in successfully", "token": session_token, "csrf_token": csrf_token}), 201                  
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

@app.route('/auth/logout', methods=['DELETE'])                                                                      #TODO, Delete the tokens
def logout_user():
    data = request.json
    session_token = sanitise_input(data['sessionToken'])

    try:
        user_auth_logout(session_token)
        return jsonify({"message": "User logged out successfully"}), 200
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

    
@app.route('/forum/new/question', methods=['POST']) 
def create_new_forum():
    data = request.json
    forum_title = sanitise_input(data['title'])
    forum_question = sanitise_input(data['forumQuestion'])
    session_token = sanitise_input(data['sessionToken'])

    try:
        user_create_forum(forum_title, forum_question, session_token)
        return jsonify({"message": "Forum created succesfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    
@app.route('/forum/retrieve', methods=['GET']) 
def retrieve_all_forums():
    try:
        forum_dict = admin_retrieve_forum_data()
        return jsonify({"message": "All forum data returned succesfully", "forums": forum_dict}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/auth/validate', methods=['POST'])
def validate_token():
    data = request.json
    session_token = sanitise_input(data['sessionToken'])

    try:
        if (user_auth_validate_token(session_token)):                                               #TODO Add CSRF Token (sess_token, CSRF_tok)
                return jsonify({"message": "Token is valid"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/forum/reply/submit', methods=['POST'])
def store_reply():
    data = request.json
    forum_id = sanitise_input(data['forumId'])
    reply_comment = sanitise_input(data['reply'])
    session_token = sanitise_input(data['sessionToken'])

    try:
        user_add_reply(forum_id, reply_comment, session_token)
        return jsonify({"message": "Forum reply added succesfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5005)

    #testing 2.3 await asyncio.sleep(10) 
    #Stops the code for 10 sec
