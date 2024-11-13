#Testcases for testing security features

#Required imports
from classes.user import *
from auth import *
import asyncio

#Pre-Testing Preparation
user = User("rkkknas@hotmail.com", "mlklk@onsdfns_.", "first_name", "last_name") #User Creation

#Testing
if __name__ == "__main__":
    
    """
    **|| Stage 1 - Basic ||** 
    """

    #1.1 - Password Hasing
    print(f"Password Hash: {user.password_hash}\n")  # Password Outputted should be hashed

    #1.2 - Input Validation
    try:
        pass
    except:
        pass