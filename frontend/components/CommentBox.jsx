import React, { useState } from 'react';
import styles from '../styles/CommentBox.module.css';

export default function CommentBox({ onPost }) {
  const [text, setText] = useState('');

  const handleChange = (event) => {
    const newText = event.target.value;
    setText(newText);       
    onPost(newText);        
  };

  return (
    <div className={styles.commentBox}>
      <textarea
        className={styles.replyInput}
        placeholder="Add comment"
        value={text}         
        onChange={handleChange}
      ></textarea>
    </div>
  );
}
