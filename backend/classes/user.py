import hashlib
import asyncio

#Token Generator
import secrets
import hmac
import hashlib
import time

#Other stuff
from general_storage import *


class User():
    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = self.hash_password(password)
        self.session_token = self.generate_token(self.email)
        self.csrf_token = self.generate_token(self.session_token)
    
    def generate_token(self, user_identifier: str) -> str: #Generates a secure Token

        random_data = secrets.token_bytes(32) #Generate 32 random bytes (256 bits)
        timestamp = int(time.time()) #Get current timestamp in seconds
        
        token_data = f"{user_identifier}-{timestamp}".encode() + random_data
    
        signature = hmac.new(SECRET_KEY.encode(), token_data, hashlib.sha256).hexdigest() #Generate HMAC signature using a secret key
         
        token = f"{token_data.hex()}-{signature}"
        
        return token

    async def validate_tokens(self, session_token, csrf_token):
        
        errors = []
        
        if self.session_token != session_token:
            errors.append("Invalid Session Token")
            
        if self.csrf_token != csrf_token:
            errors.append("Invalid CSRF Token")
        
        return errors if errors else None #Returns errors if there any, otherwise return None
            
    async def revoke_token(self):
        self.session_token = None
        self.csrf_token = None

    def hash_password(self, password_input):
        # Encode the password before hashing
        password_hashed = hashlib.sha256(password_input.encode('utf-8')).hexdigest()
        return password_hashed
    
    async def verify_password(self, password_input):

        if self.password_hash == self.hash_password(password_input):
            return(True)
        else:
            return(False)

    async def user_data(self): 
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password_hash
        }

    