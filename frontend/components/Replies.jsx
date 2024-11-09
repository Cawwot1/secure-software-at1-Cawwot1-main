// components/Replies.js
import React from 'react';
import styles from '../styles/Replies.module.css';

export default function Replies({ replies }) {
  return (
    <div className={styles.replies}>
      {replies.map((reply, index) => (
        <div key={index} className={styles.reply}>
          <p className={styles.author}>{reply.author}</p>
          <p className={styles.time}>{reply.time}</p>
          <p className={styles.replyText}>{reply.text}</p>
        </div>
      ))}
    </div>
  );
}
