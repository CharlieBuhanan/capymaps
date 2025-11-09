const form = document.getElementById('login-form');
const message = document.getElementById('login-message');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const username = form.username.value.trim();
    const password = form.password.value.trim();

    if (!username || !password) {
        message.textContent = "Please fill out both fields.";
        return;
    }

    // Example: simple client-side login mockup
    if (username === "capy" && password === "bara") {
        message.textContent = "Login successful!";
        message.style.color = "green";
        setTimeout(() => {
            window.location.href = "/static/html/map.html"; // redirect after login
        }, 800);
    } else {
        message.textContent = "Invalid credentials.";
        message.style.color = "red";
    }
});
