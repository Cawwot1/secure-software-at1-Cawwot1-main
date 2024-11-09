
import React from 'react';
import styles from '../styles/LogoutButton.module.css';

export default function LogoutButton({ onClick }) {
  return (
    <button className={styles.LogoutButton} onClick={onClick}>
      Logout
    </button>
  );
}
