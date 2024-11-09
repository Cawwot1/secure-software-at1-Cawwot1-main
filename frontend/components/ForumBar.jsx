import React from 'react';
// import styles from '../styles/Forum.module.css';
import styles from '../styles/ForumBar.module.css';


export default function ForumBar({ forums, selectedForum, onForumClick }) {
  return (
    <div className={styles.forumBar}>
      {forums.map((forum) => (
        <div
          key={forum.id}
          className={`${styles.forumOption} ${
            selectedForum === forum.title ? styles.active : ''
          }`}
          onClick={() => onForumClick(forum.title)}
        >
          <p className={styles.forumTitle}>{forum.title}</p>
          <p className={styles.forumDetails}>
           Time: {forum.time}  Replies: {forum.replies}
          </p>
        </div>
      ))}
    </div>
  );
}
