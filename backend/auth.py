from classes.user import User
from flask import abort
import re
from data import users

email_domains = [
    "@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com", "@icloud.com",
    "@aol.com", "@protonmail.com", "@zoho.com", "@yandex.com", "@gmx.com",
    "@comcast.net", "@verizon.net", "@att.net", "@sbcglobal.net", "@charter.net",
    "@cox.net", "@companyname.com", "@university.edu", "@organization.org",
    "@gov", "@mil", "@nhs.uk", "@canada.ca", "@qq.com", "@naver.com",
    "@web.de", "@orange.fr"
]

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9_]+@+.')
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_.]')
PASSWORD_PATTERN = re.compile(r'[a-zA-Z0-9_.]')

#Email Regeister Authentication - USER TOKEN

def user_auth_register(email, password, first_name, last_name):
    # Normalize the email to lowercase
    if email in users:
        abort(400, description="Email already exists")

    if not EMAIL_PATTERN.match(email):
        abort(400, description="Invalid Special Symbols in Email")

    if not PASSWORD_PATTERN.match(password):
        abort(400, description="Invalid Special Symbols in Password")

    if not USERNAME_PATTERN.match(first_name):
        abort(400, description="Invalid Special Symbols in First Name")
    
    if not USERNAME_PATTERN.match(last_name):
        abort(400, description="Invalid Special Symbols in Last Name")

    new_user = User(email, first_name, last_name, password)
    users[email] = new_user  # Store the user object by email

    return new_user.token, new_user.csrf_token                                              #Stage 2.2 Returns Newly Generated CSRF Token to SERVER.py

#Login Auth.

def user_auth_login(email, password_input):         
    email = email.lower()  # Normalize the email to lowercase
    
    if email not in users:
        abort(401, description="Email does not exist")
    
    user = users[email]
    if not user.verify_password(password_input):
        abort(401, description="Invalid password")

    # Generate a new token and update the user's token attribute
    user.token = user.generate_token(email)                                             

    # Return the new token
    return user.token, user.csrf_token                                                      #Stage 2.2 Returns CSRF Token of User to SERVER.py

def user_auth_logout(token):
    # Loop through all users in the dictionary
    for user in users.values():
        if user.token == token:  # Check if the token matches
            user.revoke_token()  # Revoke the token
            return  # Exit the function after revoking the token
    
    # If no matching token is found, abort with an error
    abort(401, description="Token does not exist")

def user_auth_validate_token(token, csrf_token): #Token Validation                                              Stage 2.1 & 2.2 - Used helper fuctions in USER.py
    
    for user in users.values():
        if user.validate_csrf_token(csrf_token) and user.validate_token(token):
            return True
        else:
            return False

if __name__ == "__main__" :
    user_auth_register("rkkknas@hotmail.com", "mlklk@onsdfns_.", "first_name", "last_name") #Testing Login Filter