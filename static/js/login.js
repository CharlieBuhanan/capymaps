const form = document.getElementById('login-form');
const message = document.getElementById('login-message');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = form.username.value.trim();
    const password = form.password.value.trim();

    if (!username || !password) {
        message.textContent = "Please fill out both fields.";
        message.style.color = "red";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Invalid credentials");
        }

        // Save the JWT token in localStorage for later API calls
        localStorage.setItem("access_token", data.access_token);

        message.textContent = "Login successful!";
        message.style.color = "green";

        setTimeout(() => {
            window.location.href = "/static/html/map.html"; // redirect after login
        }, 800);
    } catch (err) {
        message.textContent = err.message;
        message.style.color = "red";
    }
});
