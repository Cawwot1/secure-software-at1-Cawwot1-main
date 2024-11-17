import config from '../config.json';  // Import the config file
const SERVER_URL = `${config.backend.url}`;

export default async function requestValidateToken() {
    try { 
                  
        const csrf_token = localStorage.getItem('csrfToken');
        
        if (!csrf_token) {
            throw new Error('No CSRF token found');
        }

        const data = {
            csrfToken: csrf_token
        }

        const response = await fetch(SERVER_URL + '/auth/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'include': 'credentials'
            },
            body: JSON.stringify(data),
            credentials: 'include' // Include credentials (cookies) in the request
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        const result = await response.json(); 
        console.log('Response from server:', result);
        return result; 
    } catch (error) {
        console.error('Error during token validation:', error);
        return false;
    }
}

