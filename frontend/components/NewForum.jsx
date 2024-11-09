import React, { useState } from 'react';
import styles from '../styles/Forum.module.css';  // Reusing the existing Forum styles
import CommentBox from './CommentBox';
import SubmitBox from './SubmitButton';
import requestUserCreateForum from '../services/requestCreateForum'; // Import the request function

export default function NewForum({ onSubmit }) {
  const [title, setTitle] = useState('');
  const [comment, setComment] = useState('');

  const handleSubmit = async () => {
    if (title.trim() && comment.trim()) {
      onSubmit({ title, comment });
      setTitle(''); // Clear the title field
      setComment(''); // Clear the comment field
    }
    try {
      console.log(comment)
      const result = await requestUserCreateForum(title, comment);
      alert(`Created new forum!`); // Show a popup with the error message
    } catch (error) {
      alert(`New forum creation failed: ${error.message}`); // Show a popup with the error message
    }
  };

  return (
    <div className={styles.mainContent}>
      <h1 className={styles.title}>Create New Forum Post</h1>
      
      {/* Title Input */}
      <div>
        <textarea
          className={styles.newForumTitle}
          placeholder="Enter Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        ></textarea>
      </div>

      {/* Comment Box */}
      <CommentBox onPost={(text) => setComment(text)} />
      <SubmitBox onPost={handleSubmit} />
    </div>
  );
}
