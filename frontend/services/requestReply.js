import config from '../config.json';  // Import the config file
const SERVER_URL = `${config.backend.url}`;

export default async function requestReplySubmit(forumDataID, replyCommennt) {
    const token = localStorage.getItem('authToken');
    const csrf_token = localStorage.getItem('csrfToken');
    if (!token) {
        throw new Error('No token found');
    }
    const data = {
        forumId: forumDataID,
        reply: replyCommennt,
        sessionToken: token,
        csrfToken: csrf_token
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
