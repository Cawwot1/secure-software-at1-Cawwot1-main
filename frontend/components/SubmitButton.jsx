import React from 'react';
import styles from '../styles/SubmitButton.module.css';

export default function SubmitBox({ onPost }) {
    return (
        <button 
            className={styles.submitButton} 
            onClick={onPost}> Post 
        </button>
    )
}