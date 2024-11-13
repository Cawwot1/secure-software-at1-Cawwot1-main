# In-memory storage
forums = {}
users = {}

async def admin_retrieve_forum_data():
    forum_dict = {}

    # Loop through each forum in the forums dictionary
    for forum_id, forum in forums.items():
        forum_dict[forum_id] = await forum.to_dict() # Convert the forum object to a dictionary and add it to the result dictionary

    return forum_dict

async def admin_retrieve_author_name(session_token):                                                #Stage 2.2
    for _, user in users.items():  # Ignore the email (key), just get the User object               
        if user.token == session_token:
            return f"{user.first_name} {user.last_name}"
    return None

""" Old Fuction | pre 2.2
async def admin_retrieve_author_name(session_token):
    print(f"Users: {users}")
    for user_token, user_obj in users.items():
        print(user_token)
        if user_token == session_token:
            return f"{user_obj.first_name} {user_obj.last_name}"
    return None
"""