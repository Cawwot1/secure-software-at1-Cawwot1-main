import hashlib

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
        self.token = self.generate_token(email) #Session Token
        self.csrf_token = self.generate_token(self.token) #CSRF Token
    
    def generate_token(self, user_identifier: str) -> str: #Generates a secure Token

        gen_num = 0
        gen_num += 1
        print(f"Token Generation: {gen_num}")

        random_data = secrets.token_bytes(32) #Generate 32 random bytes (256 bits)
        timestamp = int(time.time()) #Get current timestamp in seconds
        
        token_data = f"{user_identifier}-{timestamp}".encode() + random_data
    
        signature = hmac.new(SECRET_KEY.encode(), token_data, hashlib.sha256).hexdigest() #Generate HMAC signature using a secret key
         
        token = f"{token_data.hex()}-{signature}"
        
        return token

    def validate_token(self, session_token): #Validates session token

        if self.token == session_token:
            return True
        else:
            return False
    
    def validate_csrf_token(self, csrf_token): #Validates csrf token
        if self.csrf_token == csrf_token:
            return True
        else:
            return False
        
    def revoke_token(self):                                                                        #Stage 2.2 | Revokes both tokens (Session & CSRF)
        print("REVOKE TOKEN")
        self.token = None
        self.csrf_token = None

    def hash_password(self, password_input):
        # Convert the password string to bytes
        password_bytes = password_input.encode('utf-8')
        # Use hashlib to create a SHA256 hash
        password_hashed = hashlib.sha256(password_bytes).hexdigest()
        return password_hashed
    
    def verify_password(self, password_input):
        
        #check
        #print(self.password_hash)
        #print(self.hash_password(password_input))
        
        if self.password_hash == self.hash_password(password_input):
            return(True)
        else:
            return(False)

    def user_data(self): 
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password_hash
        }

if __name__ == '__main__':

    # Create a new user with email and password
    user = User(email="rianni@kings.edu.au", first_name="Rocco", last_name="Ianni", password="HelloThere")

    # Verify the password
    password_attempt = "HelloThere"

    if user.verify_password(password_attempt):
        print("Password verification successful.")
    else:
        print("Password verification failed.")

    session_token = user.token
    #session_token = "123456" #Invalid Token

    # Returns TRUE for valid token
    if user.validate_token(session_token):
        print('Valid token')
    else:
        #Return FALSE for invalid token
        print('Invalid token')
    
    #CRSF Test