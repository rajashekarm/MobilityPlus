document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    }).then(function(response) {
        if (response.ok) {
            window.location.href = '/protected';
        } else {
            alert('Invalid username or password');
        }
    });
});

