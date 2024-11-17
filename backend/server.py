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

CORS(app, supports_credentials=True, origins=["http://127.0.0.1:3001"])

#XSS Sanitation
async def sanitise_input(user_input):
    # Basic HTML escaping
    return html.escape(user_input)

#Helper Token Validation Fuction
async def token_validation_helper(session_token):
    user_auth_validate_token(session_token)
    #Add CSRF Protection

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
        session_token, csrf_token = await user_auth_register(email, password, first_name, last_name)                       #Authentication Register - Stage 1.2 || Stage 2.1 & 2.2 Returns csrf_token & session token

        response = make_response(jsonify({"message": "User registered successfully", 
                                          "csrf_token": csrf_token}), 201)
        
        response.set_cookie("authToken", session_token, samesite="Lax", httponly=True, path = "/")

        return response
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 406

@app.route('/auth/login', methods=['POST']) #Logins the User, giving them a session token
async def login_user(): 
    data = request.json
    email = await sanitise_input(data['email'])
    password = await sanitise_input(data['password'])

    try:

        session_token, csrf_token = await user_auth_login(email, password)                       #Authentication Register - Stage 1.2 || Stage 2.1 & 2.2 Returns csrf_token & session token

        response = make_response(jsonify({"message": "User registered successfully", 
                                          "token": session_token, 
                                          "csrf_token": csrf_token}), 201)
        
        response.set_cookie("authToken", session_token, samesite="Lax", httponly=True, path = "/")

        return response
                  
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 401

@app.route('/auth/logout', methods=['DELETE'])                                                                      #TODO, Delete the tokens
async def logout_user():

    try:
        data = request.json
        csrf_token = await sanitise_input(data['csrfToken'])

        session_token = request.cookies.get("authToken")

        await user_auth_logout(session_token, csrf_token)

        response = make_response(jsonify({"message": "User logged out successfully"}), 200)
        response.delete_cookie("authToken")

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
    data = request.json
    csrf_token = await sanitise_input(data['csrfToken'])                                                  #Stage 2.2 | Extracts csrf Token from the LocalStorage

    session_token = request.cookies.get("authToken")

    validate_var, error_info, user_token, server_token = await user_auth_validate_token(session_token, csrf_token)               #Stage 2.2 | Splits the validation result (for more detail about errors)

    try:
        if validate_var:                                               
                return jsonify({"message": "Token & CSRF is valid"}), 200
        else:                                                                                       #Stage 2.2 | Handles Unknown & Token Errors
                if error_info == "CSRF":
                    return jsonify({"error": "Invalid CSRF Token"}), 401
                elif error_info == "Token":
                    return jsonify({"error": "Invalid Session Token"}), 401
                else:
                    return jsonify({"error": "Unknown validation error"}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500
        
@app.route('/forum/reply/submit', methods=['POST'])
async def store_reply():
    data = request.json
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
