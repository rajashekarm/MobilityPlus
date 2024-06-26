document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    var userType = document.getElementById('userType').value;
    var username = document.getElementById('uname').value;
    var password = document.getElementById('psw').value;
    var remember = document.getElementById('remember').checked; // Added remember checkbox
    fetch('/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            userType: userType,
            username: username,
            password: password,
            remember: remember // Added remember checkbox
        })
    }).then(function(response) {
        if (response.ok) {
            window.location.href = '/control';
        } else {
            alert('Invalid username, password, or user type');
        }
    });
});


function sendIdTokenToServer(idToken) {
    fetch('/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            idToken: idToken
        })
    }).then(function(response) {
        if (response.ok) {
            window.location.href = '/control';
        } else {
            alert('Failed to sign in');
        }
    });
}


/**
 * The Sign-In client object.
 */
var auth2;

/**
 * Initializes the Sign-In client.
 */
var initClient = function() {
    gapi.load('auth2', function(){
        /**
         * Retrieve the singleton for the GoogleAuth library and set up the
         * client.
         */
        auth2 = gapi.auth2.init({
            client_id: 'CLIENT_ID.apps.googleusercontent.com'
        });

        // Attach the click handler to the sign-in button
        auth2.attachClickHandler('signin-button', {}, onSuccess, onFailure);
    });
};

/**
 * Handle successful sign-ins.
 */
var onSuccess = function(user) {
    console.log('Signed in as ' + user.getBasicProfile().getName());
    // Send the ID token to your server
    sendIdTokenToServer(user.getAuthResponse().id_token);
};

/**
 * Handle sign-in failures.
 */
var onFailure = function(error) {
    console.error(error);
    // Handle `popup_closed_by_user` error
    if (error.error === 'popup_closed_by_user') {
        // You can notify the user or log this event for debugging purposes
        console.log('The sign-in popup was closed by the user.');
    }
};
