

const APIURL = 'http://localhost:8000';

async function logIn(credentials) {
    console.log("function entered")
    
    try {
        const response = await fetch(APIURL + '/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(
                credentials
            )
        });
        if (response.ok) {
            return await response.json();
        } else {
            const message = await response.text();
            throw new Error(response.statusText + " " + message);
        }
    } catch (error) {
        throw new Error(error.message, { cause: error });
    }
};

async function getUserInfo() {
    // const token = getCookie('csrftoken')
    console.log(token);
    const response = await fetch(APIURL + '/current/userInfo', {
        credentials: 'include',
        headers: {
            "X-CSRF-Token": token, 
            "Content-Type": "application/json"
          }
    });
    const user = await response.json();
    if (response.ok) {
        return user;
    } else {
        throw user;  // an object with the error coming from the server
    }
};

export {logIn, getUserInfo};