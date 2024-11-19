from classes.user import *
from flask import abort
from data import users

#Login Auth.

async def user_auth_login(email, password_input):         
    email = email.lower()  # Normalize the email to lowercase
    
    if email not in users:
        abort(401, description="Email does not exist")
    
    user = users[email]
    if not await user.verify_password(password_input):
        abort(401, description="Invalid password")

    # Generate a new token and update the user's token attribute
    user.session_token = user.generate_token(email)
    user.csrf_token = user.generate_token(user.session_token)                                       

    # Return the new token
    return [user.session_token, user.csrf_token]                                                    

async def user_auth_logout(session_token, csrf_token):                                            
    # Loop through all users in the dictionary
    for user in users.values():
        if user.session_token == session_token:  # Check if the token matches
            user.revoke_token()  # Revokes both tokens (session @ csrf)
            return  # Exit the function after revoking the token
    
    # If no matching token is found, abort with an error
    abort(401, description="Token does not exist")

async def user_auth_validate_token(session_token, csrf_token): #Token Validation                                              
    
    for user in users.values():
        if session_token == user.session_token:
            if await user.validate_tokens(session_token, csrf_token) == None:
                return True, "no error" #All Valid
            else:
                return False, "CSRF" #Invalid CSRF
        else:
            pass
        
        return True, "Session" #Invalid Session