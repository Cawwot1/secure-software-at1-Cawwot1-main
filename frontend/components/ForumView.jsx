import React, { useState } from 'react';
import styles from '../styles/Forum.module.css';
import CommentBox from './CommentBox';
import Replies from './Replies';
import SubmitBox from './SubmitButton';
import requestReplySubmit from '../services/requestReply';
import requestForumData from '../services/requestForumData';

export default function ForumContent({ selectedForumData }) {
  const [comment, setComment] = useState(''); 
  const [replies, setReplies] = useState([...selectedForumData.question.replies]); // Ensure new array reference

  const fetchUpdatedForumData = async (forumId) => {
    try {
      const forumDataArray = await requestForumData(); 
      const updatedForumData = forumDataArray.find(forum => forum.id === forumId); 
  
      if (updatedForumData && updatedForumData.question) {
        // Create a new array reference to force a re-render
        setReplies([...updatedForumData.question.replies]);
      } else {
        console.error("Updated forum data is missing the question or replies field");
      }
    } catch (error) {
      console.error("Error fetching updated forum data:", error);
    }
  };

  const handleReplySubmit = async () => {
    if (!comment.trim()) {
      alert('Reply cannot be empty.');
      return;
    }

    const forumId = selectedForumData.id;
    
    try {
      const response = await requestReplySubmit(forumId, comment);
      if (response.message === 'Forum reply added successfully') {
        setComment(''); // Reset comment box
        console.log("Submission of forum reply successful");
        await fetchUpdatedForumData(forumId); // Fetch updated replies from the server after submission
      } else {
        console.error("Error submitting reply:", response);
      }
    } catch (error) {
      console.error("Error occurred during reply submission:", error);
    }
  };

  return (
    <div className={styles.mainContent}>
      <h1 className={styles.title}>{selectedForumData.title}</h1>
      
      {/* Submitted Question Display */}
      <div className={styles.post}>
        <p className={styles.author}>{selectedForumData.author}</p>
        <p className={styles.time}>{selectedForumData.question.time}</p>
        <p className={styles.question}>{selectedForumData.question.text}</p>
      </div>

      {/* Comment Box */}
      <CommentBox onPost={setComment} value={comment} />

      {/* Submit Button */}
      <SubmitBox onPost={handleReplySubmit}>Reply</SubmitBox>

      {/* Indented Replies */}
      <Replies replies={replies} /> {/* Use the updated replies state */}
    </div>
  );
}
