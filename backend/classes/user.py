import hashlib
import asyncio

#Token Generator
import secrets
import hmac
import hashlib
import time

#Other stuff
from general_storage import *

"""
The User object, initialised when a user registers, is the object storing information about the user

There are various methods related to token generation, validation, removal and password hashing

1. generate_token - generates the session & csrf tokens
2. validate_token - validates inputted token to see if it matches tokens stored in the user class
3. revoke_tokens - removes token (to be used when logging out)
4. hash_password - hashes the user password
5. verify_password - checks if the hashed inputted password matches the stored password
6. user_data - returns some user data: email, first_name, last_name and password
"""

class User(): #The User Class
    def __init__(self, email, first_name, last_name, password): #Information from the registration page is inputted into the class
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = self.hash_password(password) #Hashes the password based on the sha256 hash algorithm
        self.session_token = self.generate_token(self.email) #Generates a new token based on the user email, a random secret key and the timestamp
        self.csrf_token = self.generate_token(self.session_token) #Refactors the session token to generate the csrf token
    
    def generate_token(self, user_identifier: str) -> str: #Generates a secure Token

        random_data = secrets.token_bytes(32) #Generate 32 random bytes (256 bits)
        timestamp = int(time.time()) #Get current timestamp in seconds
        
        token_data = f"{user_identifier}-{timestamp}".encode() + random_data
    
        signature = hmac.new(SECRET_KEY.encode(), token_data, hashlib.sha256).hexdigest() #Generate HMAC signature using a secret key
         
        token = f"{token_data.hex()}-{signature}"
        
        return token

    async def validate_tokens(self, session_token, csrf_token): #Checks if the given tokens are equal to the tokens stored in the user
        
        errors = [] #error information
        
        if self.session_token != session_token: 
            errors.append("Invalid Session Token")
            
        if self.csrf_token != csrf_token:
            errors.append("Invalid CSRF Token")
        
        return errors if errors else None #Returns errors if there any, otherwise return None
            
    async def revoke_token(self): #Removes csrf_token from the user
        self.csrf_token = None

    def hash_password(self, password_input): #hashes the password using sha256
        # Encode the password before hashing
        password_hashed = hashlib.sha256(password_input.encode('utf-8')).hexdigest()
        return password_hashed
    
    async def verify_password(self, password_input): #Checks if the given password is equal to the stored password once it is hashed

        if self.password_hash == self.hash_password(password_input):
            return(True)
        else:
            return(False)

    async def user_data(self): #User data, not containing any important information
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            #'password': self.password_hash 
        }

    