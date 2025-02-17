const API_URL = "http://127.0.0.1:4000"; // Upewnij się, że port się zgadza!

function showTab(tab) {
    const loginButton = document.querySelector(".tab-button:first-child");
    const registerButton = document.querySelector(".tab-button:last-child");

    if (tab === "login") {
        document.getElementById("login-form").classList.remove("hidden");
        document.getElementById("register-form").classList.add("hidden");
        loginButton.classList.add("active");
        registerButton.classList.remove("active");
    } else {
        document.getElementById("register-form").classList.remove("hidden");
        document.getElementById("login-form").classList.add("hidden");
        registerButton.classList.add("active");
        loginButton.classList.remove("active");
    }
}

    function register() {
    const name = document.getElementById("register-name").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    fetch(`${API_URL}/users`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password
        })
    })
    .then(response => {
        console.log("Response status:", response.status);
        return response.json();
    })
    .then(data => {
        if (data.id) {
            alert("User registered successfully! You can now log in.");
            showTab("login"); // Przełączenie na zakładkę logowania
        } else {
            alert("Registration failed: " + (data.detail || "Unknown error"));
        }
    })
    .catch(error => console.error("Error:", error));
}

async function login() {
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,  // 🚀 SPRAWDŹ, CZY API OCZEKUJE `email`, NIE `username`
                password: password
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Login failed");
        }

        const data = await response.json();
        console.log("Token received:", data.access_token);
        localStorage.setItem("token", data.access_token);
        alert("Login successful!");

    } catch (error) {
        console.error("Login error:", error);
        alert(error.message);
    }
}

function getUserData() {
    const token = localStorage.getItem("token");
    if (!token) {
        alert("No token found, please log in first.");
        return;
    }

    fetch(`${API_URL}/users/me`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("User data:", data);
        alert(`Logged in as: ${data.email}`);
    })
    .catch(error => console.error("Error:", error));
}
