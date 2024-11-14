const response = await fetch(SERVER_URL + '/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                //'Authorization': `session token ${token}`, //ADDDED
                //'CSRF Token': `csrf token ${csrf_token}` //ADDDED  
            },