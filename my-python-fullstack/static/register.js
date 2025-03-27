function validateEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
}



function getValue() {
    const inputAge = document.getElementById("age");
    const inputName = document.getElementById("name");
    const inputEmail = document.getElementById("email");
    const inputPassword = document.getElementById("password");

    // Get values
    const age = inputAge.value;
    const name = inputName.value;
    const email = inputEmail.value;
    const password = inputPassword.value;

    // Validate inputs
    if (!name || !email || !password) {
        alert('Name, email, and password are required fields!');
        return;
    }

    if (!validateEmail(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    const userDetails = {
        name: name,
        email: email,
        password: password,
        age: age
    };

    console.log("User Details:", JSON.stringify(userDetails, null, 2));

    // Send the userDetails object to the backend via a POST request
    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userDetails)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(`${name} Registration successful!`);

                // ✅ Clear input fields after successful registration
                inputAge.value = "";
                inputName.value = "";
                inputEmail.value = "";
                inputPassword.value = "";
                window.location.reload();
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.');
        });
}

//fetch user  api

function fetchUsers() {
    // console.log("Fetching users...");
    fetch("http://127.0.0.1:5000/users")
        .then(response => response.json())
        .then(users => {
            console.log("API Response:", users);
            

            let tableBody = document.getElementById("containers");

            tableBody.innerHTML = users.map((user, index) => `
        <tr>
            <td>${index + 1}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.password}</td>
            <td>${user.age}</td>
            <td><button onclick="deleteUser('${user.email}')" class='delete-btn'>Delete</button></td>
             <td><button onclick="updateUser('${user.email}')" class='edit-btn'>Edit</button></td>
        </tr>
    `).join("");
            console.log("Users loaded successfully!");
        })
        .catch(error => console.error("Error fetching users:", error));
}

function deleteUser(email) {
    if (!confirm("Are you sure you want to delete this user?")) return;

    fetch(`http://127.0.0.1:5000/delete/${email}`, {
        method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show success or error message
        fetchUsers(); // Refresh the user list
    })
    .catch(error => console.error("Error deleting user:", error));
}



function updateUser(email) {
    let name = prompt("Enter new name:");
    let password = prompt("Enter new password:");
    let age = prompt("Enter new age:");

    if (!name || !password || !age) {
        alert("All fields are required!");
        return;
    }

    fetch(`http://127.0.0.1:5000/update/${email}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, password, age })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show success message
        fetchUsers(); // Refresh the user list
    })
    .catch(error => console.error("Error updating user:", error));
}

