import React, { useState } from 'react';
import styles from '../styles/Forum.module.css';
import ThreadButton from '../components/ThreadButton';
import ForumBar from '../components/ForumBar';
import ForumContent from '../components/ForumView';
import NewForum from '../components/NewForum';
import LogoutButton from '../components/LogoutButton';
import useAuthentication from '../hooks/useAuthentication';
import useForumData from '../hooks/useForumData';
import useLogout from '../hooks/useLogout';

export default function Forum() {
  const isAuthenticated = useAuthentication();
  const [forums, setForums] = useForumData();
  const [view, setView] = useState('forum');
  const [selectedForum, setSelectedForum] = useState('Special Cons');
  const logout = useLogout();

  if (!isAuthenticated) return null;

  const handleForumClick = (forumTitle) => {
    setSelectedForum(forumTitle);
    setView('forum');
  };

  const handleCreatePost = ({ title, comment }) => {
    const newForum = {
      id: forums.length + 1,
      title: title,
      time: 'just now',
      author: 'Current User',
      replies: 0,
      question: {
        time: 'just now',
        text: comment,
        replies: [],
      },
    };

    setForums([...forums, newForum]);
    setSelectedForum(newForum.title);
    setView('forum');
  };

  const selectedForumData = forums.find((forum) => forum.title === selectedForum);

  return (
    <div className={styles.forumContainer}>
      <div className={styles.sidebar}>
        <ThreadButton onClick={() => setView('create')} />
        <LogoutButton onClick={logout} />
        <ForumBar forums={forums} selectedForum={selectedForum} onForumClick={handleForumClick} />
      </div>

      {view === 'forum' && selectedForumData && (
        <ForumContent selectedForumData={selectedForumData} />
      )}

      {view === 'create' && (
        <NewForum onSubmit={handleCreatePost} />
      )}
    </div>
  );
}
