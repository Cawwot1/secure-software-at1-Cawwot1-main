import hashlib

class User():
    def __init__(self, email, first_name, last_name, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = self.hash_password(password)
        self.token = self.generate_token(email)
    
    def generate_token(self, email):
        return self.email
    
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
    
# Create a new user with email and password
user = User(email="rianni@kings.edu.au", first_name="Rocco", last_name="Ianni", password="HelloThere")

# Verify the password
password_attempt = "HelloThere"

if user.verify_password(password_attempt):
    print("Password verification successful.")
else:
    print("Password verification failed.")