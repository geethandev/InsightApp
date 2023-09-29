const signupForm = document.getElementById("signup-form");
const messageElement = document.getElementById("message");

signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/signup/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, email, password }),
        });

        if (response.status === 201) {
            messageElement.textContent = "Signup successful! Redirecting to login...";
            
            // Redirect to the login page after a short delay (2 seconds)
            setTimeout(() => {
                window.location.replace("/login/");
            }, 2000);
        } else if (response.status === 400) {
            messageElement.textContent = "Email or username already exists. Please use another email or username.";
        } else {
            messageElement.textContent = "Signup failed. Please try again.";
        }
    } catch (error) {
        console.error("Error:", error);
    }
});
