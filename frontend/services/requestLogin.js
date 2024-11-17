import config from '../config.json';  // Import the config file
const SERVER_URL = `${config.backend.url}`;

export default async function requestUserAuthLogin(email, password) {
    const data = {
        email: email,
        password: password,  
    };

    try { 
        const response = await fetch(SERVER_URL + '/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'include': 'credentials'
                //'Authorization': `session token ${token}`, //ADDDED
                //'CSRF Token': `crsf token ${csrf_token}` //ADDDED                           
            },
            body: JSON.stringify(data),
            credentials: 'include' // Include credentials (cookies) in the request
        });

        // Check if the response is not OK 
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        const result = await response.json(); // Parse JSON response

        return result.csrf_token; // Return the token if registration is successful                           Stage 2.2 Added "result.csrf_token" to return it to local storage
    } catch (error) {
        console.error('Error during registration:', error);
        throw error; // Re-throw the error so it can be handled in handleSubmit
    }
}
