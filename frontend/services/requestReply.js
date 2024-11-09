import config from '../config.json';  // Import the config file
const SERVER_URL = `${config.backend.url}`;

export default async function requestReplySubmit(formumDataID, replyCommennt) {
    const token = localStorage.getItem('authToken');
    if (!token) {
        throw new Error('No token found');
    }
    const data = {
        forumId: formumDataID,
        reply: replyCommennt,
        sessionToken: token
    };

    try { 
        const response = await fetch(SERVER_URL + '/forum/reply/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        // Check if the response is not OK 
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        const result = await response.json(); // Parse JSON response
        return result; 
    } catch (error) {
        console.error('Error during registration:', error);
        throw error; 
    }
}
