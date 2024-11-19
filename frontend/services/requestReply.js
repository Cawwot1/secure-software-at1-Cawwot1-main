import config from '../config.json';  // Import the config file
const SERVER_URL = `${config.backend.url}`;

export default async function requestReplySubmit(forumDataID, replyComment) {
    
    //Testing Issue | No reply data
    console.log(`Forum Data: ${forumDataID}, Reply Comment: ${replyComment}`)

    const data = {
        forumId: forumDataID,
        reply: replyComment
    };

    //console.log(data) | Correct

    try { 
        const response = await fetch(SERVER_URL + '/forum/reply/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
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
