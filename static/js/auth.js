// auth.js
export async function checkAuth() {
    const token = localStorage.getItem("access_token");
    if (!token) {
        // ❌ No token — send them to login
        window.location.href = "./login.html";
        return;
    }

    try {
        // 🧭 Try to call a protected endpoint to verify the token.
        // You can use /markers (requires auth) or create a small /me endpoint.
        const response = await fetch("http://127.0.0.1:8000/markers", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });

        if (response.status === 401) {
            // ❌ Invalid or expired token — clear and redirect
            localStorage.removeItem("access_token");
            localStorage.removeItem("token_type");
            window.location.href = "./login.html";
        }
    } catch (error) {
        console.error("Auth check failed:", error);
        window.location.href = "./login.html";
    }
}
