import config from '../config.json';  // Import the config file
const SERVER_URL = `${config.backend.url}`;

export default async function requestUserAuthRegister(email, password, firstName, lastName) {
    const data = {
        email: email,
        password: password,  
        firstName: firstName,
        lastName: lastName
    };

    try { 
        const response = await fetch(SERVER_URL + '/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        });
   
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        const result = await response.json(); // Parse JSON response
        console.log('Response from server:', result);
        return result.token; // Return the token if registration is successful
    } catch (error) {
        console.error('Error during registration:', error);
        throw error; // Re-throw the error so it can be handled in handleSubmit
    }
}
