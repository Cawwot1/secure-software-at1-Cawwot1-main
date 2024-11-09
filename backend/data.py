# In-memory storage
forums = {}
users = {}

def admin_retrieve_forum_data():
    forum_dict = {}

    # Loop through each forum in the forums dictionary
    for forum_id, forum in forums.items():
        forum_dict[forum_id] = forum.to_dict() # Convert the forum object to a dictionary and add it to the result dictionary

    return forum_dict

def admin_retrieve_author_name(session_token):
    for user_token, user_obj in users.items():
        if user_token == session_token:
            return f"{user_obj.first_name} {user_obj.last_name}"
    return None