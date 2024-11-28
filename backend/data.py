# In-memory storage
forums = {}
users = {}

"""
This is where the forum data is stored

admin_retrieve_forum_data - returns all data in forum
admin_retrieve_author_name - looks for the name of the author using the session token
"""

async def admin_retrieve_forum_data():
    # Initialize an empty dictionary to store forum data
    forum_dict = {}

    # Loop through each forum in the 'forums' dictionary
    for forum_id, forum in forums.items():
        # Convert each forum object to a dictionary using its 'to_dict()' method
        # Store the result in the 'forum_dict' under the respective forum_id
        forum_dict[forum_id] = await forum.to_dict()

    # Return the complete dictionary containing all forum data
    return forum_dict

async def admin_retrieve_author_name(session_token, csrf_token):                                              
    for _, user in users.items():  # Ignore the email (key), just get the User object               
        if user.session_token == session_token and user.csrf_token == csrf_token:
            return f"{user.first_name} {user.last_name}"
    return None