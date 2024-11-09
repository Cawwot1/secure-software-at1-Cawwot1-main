from datetime import datetime

class Forum:
    def __init__(self, id, title, author, question_text):
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

    def add_reply_to_question(self, author, text):
        reply = {'author': author, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'text': text}
        self.question['replies'].append(reply)
        self.replies += 1  # Increment the number of replies

    def to_dict(self):
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
    
    def __repr__(self):
        return f"Forum(ID: {self.id}, Title: '{self.title}')"
