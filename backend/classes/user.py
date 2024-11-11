import hashlib

#Token Generator
import secrets
import hmac
import hashlib
import time

#Other stuff - Add to another file
SECRET_KEY = "d4f8e19cfa6a4c748e583234e905849f0c7b2f3e5db8ab3cdd4f5b6d1e2f3c4b"

class User():
    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = self.hash_password(password)
        self.token = self.generate_token(email, SECRET_KEY)
    
    def generate_token(self, user_email: str, secret_key: str) -> str: #Generates a secure Token
        
        random_data = secrets.token_bytes(32) #Generate 32 random bytes (256 bits)
        timestamp = int(time.time()) #Get current timestamp in seconds
        
        token_data = f"{user_email}-{timestamp}".encode() + random_data
    
        signature = hmac.new(secret_key.encode(), token_data, hashlib.sha256).hexdigest() #Generate HMAC signature using a secret key
         
        token = f"{token_data.hex()}-{signature}"
        
        return token
    
    def revoke_token(self):
        self.token = None

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
    
    #User Token
    print(user.token)