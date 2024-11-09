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
        console.log('Result token: ', result.token);
        return result.token; 
    } catch (error) {
        console.error('Error during registration:', error);
        throw error; // Re-throw the error so it can be handled in handleSubmit
    }
}
