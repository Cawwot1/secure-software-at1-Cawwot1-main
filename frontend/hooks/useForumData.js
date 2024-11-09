import { useEffect, useState } from 'react';
import requestForumData from '../services/requestForumData';

export default function useForumData() {
  const [forums, setForums] = useState([]);

  useEffect(() => {
    const fetchForumData = async () => {
      try {
        const retrievedForums = await requestForumData();
        setForums(retrievedForums);
      } catch (error) {
        alert(`Forum data retrieval failed: ${error.message}`);
      }
    };

    fetchForumData();
  }, []);

  return [forums, setForums];
}
