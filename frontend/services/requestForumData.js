import config from '../config.json';
const SERVER_URL = `${config.backend.url}`;

export default async function requestForumData() {
    try { 
        const response = await fetch(`${SERVER_URL}/forum/retrieve`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        // Check if the response is OK 
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Unknown error occurred');
        }

        const result = await response.json(); 

        // Convert the JSON dictionary to an array of objects
        const forumsArray = Object.keys(result.forums).map(key => result.forums[key]);
        console.log(forumsArray)

        return forumsArray;

    } catch (error) {
        console.error('Error during data retrieval:', error);
        throw error;
    }
}
