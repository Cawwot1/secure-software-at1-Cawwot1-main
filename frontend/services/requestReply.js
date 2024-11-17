import config from '../config.json';  // Import the config file
const SERVER_URL = `${config.backend.url}`;

export default async function requestReplySubmit(forumDataID, replyComment) {
    
    const csrf_token = localStorage.getItem('csrfToken');
    
    //Testing Issue | No reply data
    console.log(`Forum Data: ${forumDataID}, Reply Comment: ${replyComment}`)

    if (!csrf_token) {
        throw new Error('No CSRF token found');
    }
    const data = {
        forumId: forumDataID,
        reply: replyComment,
        csrfToken: csrf_token
    };

    //console.log(data) | Correct

    try { 
        const response = await fetch(SERVER_URL + '/forum/reply/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'include': 'credentials'
            },
            body: JSON.stringify(data),
            credentials: 'include'
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
