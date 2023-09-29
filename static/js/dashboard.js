document.addEventListener("DOMContentLoaded", async function() {
    // Get the user's token from localStorage
    const token = localStorage.getItem("token");
    if (!token) {
        // Handle the case where there's no token (user not logged in)
        console.error("User not logged in.");
    } else {
        // Add an event listener to the logout button
        const logoutButton = document.getElementById("logout-button");
        logoutButton.addEventListener("click", function() {
            // Clear the token from localStorage
            localStorage.removeItem("token");
            // Redirect to the login page
            window.location.href = "/"; // Update with your login page URL
        });

        // Fetch and set the user's avatar image
        const response = await fetch("/dashboard/user/avatar", {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (response.status === 200) {
            // Set the response data as the source of the avatar image
            const avatarImg = document.getElementById("avatar");
            avatarImg.src = URL.createObjectURL(await response.blob());
        } else {
            console.error("Failed to fetch user avatar.");
        }

        // Add a click event listener to the avatar image to open the user profile modal
        const avatarImg = document.getElementById("avatar");
        avatarImg.addEventListener("click", function() {
            // Fetch and display user profile data
            fetch("/user/profile", {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then(response => response.json())
            .then(data => {
                // Update the user profile modal content with the retrieved data
                document.getElementById("modalAvatar").src = avatarImg.src; // Update with your avatar URL
                document.getElementById("modalUsername").textContent = data.username;
                document.getElementById("modalEmail").textContent = data.email;
            })
            .catch(error => {
                console.error("Error fetching user profile:", error);
            });

            // Show the user profile modal
            $("#userProfileModal").modal("show");
        });
    }
});
