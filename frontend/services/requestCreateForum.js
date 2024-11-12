import config from '../config.json';
const SERVER_URL = `${config.backend.url}`;

export default async function requestUserCreateForum(title, forumQuestion) {
    const token = localStorage.getItem('authToken');
    const csrf_token = localStorage.getItem('csrfToken');
    
    console.log(`Session Token after login is ${token}
        CSRF Token after login is ${csrf_token}`)
    
    if (!token || !csrf_token) {
        throw new Error('No token found');
    }

    const data = {
        title: title,
        forumQuestion: forumQuestion, 
        sessionToken: token,
        csrfToken: token
    };

    try { 
        const response = await fetch(SERVER_URL + '/forum/new/question', {
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

        const result = await response.json(); 
        console.log('Response from server:', result);
        return {};
    } catch (error) {
        console.error('Error during registration:', error);
        throw error;
    }
}
