from flask import abort
from datetime import datetime
from classes.forum import Forum
from data import forums, users, admin_retrieve_author_name
from classes.user import User

# Dictionary to store forums by their numeric ID
next_forum_id = 1  # This will serve as our auto-incrementing ID

async def user_create_forum(forum_title, forum_question, session_token):
    global next_forum_id
    # Create a new Forum object

    author = await admin_retrieve_author_name(session_token)
    new_forum = Forum(
        id=next_forum_id,
        title=forum_title,
        author=author,  # Replace with actual user logic if needed
        question_text=forum_question
    )
    # Store the new forum in the dictionary using the numeric ID
    forums[next_forum_id] = new_forum
    # Increment the ID for the next forum
    next_forum_id += 1

    return new_forum.id

async def user_add_reply(forum_id, reply_text, session_token):
    
    target_forum = None  # Initialize target_forum as None

   # Loop through the forums dictionary to find the matching forum ID
    for fid, forum in forums.items():
        
        print(f"FID: {fid}\nForumID: {forum_id} \nForum: {forum}")                         
        
        if str(fid) == str(forum_id):
            target_forum = forum
            
            print(target_forum)                                                             
            
            break  # Exit the loop once the forum is found

    print("target_forum after loop:", target_forum)   

    if not target_forum:
        abort(404, description="Forum found with invalid forum id")

    # Retrieve the author from the users dictionary using the session token
    author = await admin_retrieve_author_name(session_token)

    #print(f"Session Token {session_token}\nAuthor: {author}")                              TEST

    if not author:
        abort(401, description="Invalid session token")

        
    # Add the reply to the found forum
    await target_forum.add_reply_to_question(author, reply_text)
    for index, reply in enumerate(target_forum.question['replies'], start=1):
                print(f"Reply {index}:")
                print(f"  Author: {reply['author']}")
                print(f"  Time: {reply['time']}")
                print(f"  Text: {reply['text']}")
                print()  # Blank line for readability

    print(f"Reply added to forum ID: {forum_id}")
    return True
