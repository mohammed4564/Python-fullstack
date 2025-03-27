function validateEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
}

function getValue() {
    const inputage = document.getElementById("age").value;
    const inputname = document.getElementById("name").value;
    const inputemail = document.getElementById("email").value;
    const inputpassword = document.getElementById("password").value;

    // Validate inputs
    if (!inputname || !inputemail || !inputpassword) {
        alert('Name, email, and password are required fields!');
        return;
    }

    if (!validateEmail(inputemail)) {
        alert('Please enter a valid email address.');
        return;
    }

    const userdetails = {
        name: inputname,
        email: inputemail,
        password: inputpassword,
        age: inputage
    };

    console.log("User Details:", JSON.stringify(userdetails, null, 2));

    // Send the userdetails object to the backend via a POST request
    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userdetails)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert('Registration successful!');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
    });
}
