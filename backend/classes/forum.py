from datetime import datetime

"""
The Forum class, which can be used to generate a forum

The class also has a few methods:

1. add_reply_to_question which adds a reply to the forum
2. to_dict which returns the data of the forum in the form of a dictionary
3. __repr__ which sets that is displayed when a initalised forum object is printed
"""

class Forum:
    def __init__(self, id, title, author, question_text): #Forum class, when called generates a new forum object
        self.id = id
        self.title = title
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        self.author = author
        self.replies = 0
        self.question = {
            'text': question_text,
            'time': self.time,  # Set the question time when the forum is created
            'replies': []  # Initialize with an empty list for replies
        }

    async def add_reply_to_question(self, author, text): #Adds a new reply to the forum
        reply = {'author': author, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'text': text}
        self.question['replies'].append(reply)
        self.replies += 1  # Increment the number of replies

    async def to_dict(self): #Returns forum data
        return {
            'id': self.id,
            'title': self.title,
            'time': self.time,
            'author': self.author,
            'replies': self.replies,
            'question': {
                'time': self.question['time'],  # Now this field exists in self.question
                'text': self.question['text'],
                'replies': [reply for reply in self.question['replies']]
            }
        }
    
    def __repr__(self): #The information that is returned when the object is printed (one it has been initialised)
        return f"Forum(ID: {self.id}, Title: '{self.title}')"
