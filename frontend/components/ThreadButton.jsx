
import React from 'react';
import styles from '../styles/ThreadButton.module.css';

export default function ThreadButton({ onClick }) {
  return (
    <button className={styles.ThreadButton} onClick={onClick}>
      Create Thread
    </button>
  );
}
