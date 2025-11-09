const form = document.getElementById('signup-form');
const message = document.getElementById('signup-message');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = form.username.value.trim();
    const password = form.password.value.trim();
    const instagram = form.instagram.value.trim() || null;

    message.style.color = "red";
    message.textContent = "";

    if (!username || !password) {
        message.textContent = "Please fill out all required fields.";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password, instagram }),
        });

        const data = await response.json();

        if (!response.ok) {
            if (Array.isArray(data.detail)) {
                message.textContent = data.detail.map(err => err.msg || err).join(", ");
            } else {
                message.textContent = data.detail || "Sign-up failed.";
            }
            return;
        }

        message.style.color = "green";
        message.textContent = "Account created successfully! Please head to login.";

        // setTimeout(() => {
        //     window.location.href = "./login.html";
        // }, 1200);

    } catch (error) {
        console.error("Signup error:", error);
        message.textContent = "Error connecting to server.";
    }
});
