#Testcases for testing security features

#Required imports
from classes.user import *
from auth import *
import asyncio
from server import *

"""Other Info

User Object Creation ->  (email, first_name, last_name, password)

"""

"""
**|| Stage 1 - Basic ||** 
"""

#1.1 - Password Hashing Test
def password_hash_test():
    print("\n\033[1m\033[4mPassword Hashing Test\033[0m")

    password = input("\nInput Password: ")

    user = User("rkkknas@hotmail.com", "first_name", "last_name", password)

    return user.password_hash #Returns hashed password
    
""""""

#1.2 - Input Validation Test
async def input_validation_test():

    print("\n\033[1m\033[4mInput Validation Test\033[0m")

    email = input("\nInput User Email: ")
    password = input("Input User Password: ")
    first_name = input("Input First Name: ")
    last_name = input("Input Last Name: ")

    try:
        await user_auth_register(email, first_name, last_name, password)
    except Exception as e:
        print(f"\nCaught expected input validation error: {e}")
        
        """
        print(f"\nEmail: {email}"
              f"\nPassword: {password}"
              f"\nFirst Name: {first_name}"
              f"\nLast Name: {last_name}")
        """

""""""

#1.3 - SQL Injection Test
async def sql_injection_test():

    print("\n\033[1m\033[4mSQL Injection Test\033[0m")
    
    print("\nNote: SQL Injection cannot be directly testing in backend, so its using the fuction that all inputs would go through")

    sql_injection = input("\nInput SQL Injection (into first name): ")

    return await sanitise_input(sql_injection)

""""""

#2.1 & 2.2 - Session Management & CSRF
async def session_management_test():

    print("\n\033[1m\033[4mSession Management\033[0m")
    
    email = input("\nInput User Email: ")
    password = input("Input User Password: ")
    first_name = input("Input First Name: ")
    last_name = input("Input Last Name: ")

    session_token, csrf_token = await user_auth_register(email, password, first_name, last_name)

    print(f"\nSession Token: {session_token}")
    print(f"\nCSRF Token: {csrf_token}")

    session_val = input("\nRun Session Token Validation? (Y/N) ")
    
    if session_val.lower().replace(" ","") == "y":
        try:
            
            session_token = input("\nInput Session Token: ")
            csrf_token = input("\nInput CSRF Token: ")

            await user_auth_validate_token(session_token.replace(" ",""), csrf_token.replace(" ",""))
            print("\nNo Token Errors in Validation")
        except Exception as e:
            print(f"\nCaught expected input validation error: {e}")

""""""

if __name__ == "__main__":

    # Pre-Testing Preparation
    user = User("rkkknas@hotmail.com", "first_name", "last_name", "banana")

    #Tests
    print(f"\nHashed Passwod: {password_hash_test()}") #1.1

    asyncio.run(input_validation_test()) #1.2

    print(f"\nSantisied Script: {asyncio.run(sql_injection_test())}") #1.3

    asyncio.run(session_management_test()) #2.1

    #Other Stage
    #2.3 - Isn't Required
    #3.1 - Cannot prove: can see in pages (e.g. in login.js)
    #3.2 - Cannot prove: can see when inspecting page after login (in applications -> cookies)

    

    