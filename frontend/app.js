function isAuthenticated() {

    const token =
        localStorage.getItem("access_token");

    if (!token) {

    return false;
    }

    if (isTokenExpired(token)) {

    localStorage.clear();

    return false;
    }

return true;
}

function parseJwt(token) {

    try {

        return JSON.parse(
            atob(token.split('.')[1])
        );

    } catch (e) {

        return null;
    }
}

function isTokenExpired(token) {

    const decoded = parseJwt(token);

    if (!decoded) {

        return true;
    }

    const currentTime =
        Date.now() / 1000;

    return decoded.exp < currentTime;
}

const API_BASE = "http://127.0.0.1:8000";


// =========================
// REGISTER SYSTEM
// =========================

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const username =
            document.getElementById("username").value;

        const email =
            document.getElementById("email").value;

        const password =
            document.getElementById("password").value;

        const confirmPassword =
            document.getElementById("confirmPassword").value;

        const message =
            document.getElementById("message");

        message.innerText = "";

        if (password !== confirmPassword) {

            message.style.color = "red";

            message.innerText =
                "Passwords do not match";

            return;
        }

        try {

            const response = await fetch(
                `${API_BASE}/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        username,
                        email,
                        password
                    })
                }
            );

            const data = await response.json();

            if (response.ok) {

                message.style.color = "lightgreen";

                message.innerText =
                    "Registration successful. Redirecting to login...";

                setTimeout(() => {

                    window.location.href =
                        "index.html";

                }, 2000);

            } else {

                message.style.color = "red";

                message.innerText =
                    data.detail || "Registration failed";
            }

        } catch (error) {

            message.style.color = "red";

            message.innerText =
                "Server connection failed";
        }
    });
}


// =========================
// LOGIN SYSTEM
// =========================

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const email =
            document.getElementById("email").value;

        const password =
            document.getElementById("password").value;

        const message =
            document.getElementById("message");

        message.innerText = "";

        try {

            const response = await fetch(
                `${API_BASE}/login`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email,
                        password
                    })
                }
            );

            const data = await response.json();

            if (data.access_token) {

                localStorage.setItem(
                    "access_token",
                    data.access_token
                );

                localStorage.setItem(
                    "refresh_token",
                    data.refresh_token
                );

                message.style.color = "lightgreen";

                message.innerText =
                    "Login successful. Redirecting...";

                setTimeout(() => {

                    window.location.href =
                        "dashboard.html";

                }, 1000);

            } else {

                message.style.color = "red";

                message.innerText =
                    data.detail || "Login failed";
            }

        } catch (error) {

            message.style.color = "red";

            message.innerText =
                "Server connection failed";
        }
    });
}


// =========================
// LOAD PROFILE
// =========================

async function loadProfile() {

    const token =
        localStorage.getItem("access_token");

    if (!token) {

        window.location.href = "index.html";

        return;
    }

    try {

        const response = await fetch(
            `${API_BASE}/profile`,
            {
                method: "GET",

                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        if (data.user_data) {

            document.getElementById("userInfo").innerHTML = `
                <strong>Email:</strong> ${data.user_data.sub}<br>
                <strong>User ID:</strong> ${data.user_data.user_id}
            `;

        } else {

            localStorage.clear();

            window.location.href =
                "index.html";
        }

    } catch (error) {

        localStorage.clear();

        window.location.href =
            "index.html";
    }
}


// =========================
// LOGOUT SYSTEM
// =========================

function logout() {

    localStorage.clear();

    window.location.href =
        "index.html";
}


// =========================
// AUTO LOAD DASHBOARD
// =========================

if (
    window.location.pathname.includes(
        "dashboard.html"
    )
) {

    if (!isAuthenticated()) {

        window.location.href =
            "index.html";

    } else {

        loadProfile();
    }
}

async function goTo2FA() {

    console.log("2FA button clicked");

    const token =
        localStorage.getItem("access_token");

    try {

        const response = await fetch(
            `${API_BASE}/enable-2fa`,
            {
                method: "POST",

                headers: {
                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );

        console.log("Response received");

        const data = await response.json();

        console.log(data);

        if (data.qr_code_path) {

            alert(
                "QR Code Generated.\n\n" +
                "Open backend/logs folder and scan QR code."
            );

            console.log("Redirecting now");

            window.location.href =
                "http://127.0.0.1:5500/frontend/verify-2fa.html";

        } else {

            alert("Failed to enable 2FA");
        }

    } catch (error) {

        console.error(error);

        alert("Server connection failed");
    }
}

const verify2FAForm =
    document.getElementById("verify2FAForm");

if (verify2FAForm) {

    verify2FAForm.addEventListener(
        "submit",
        async (e) => {

            e.preventDefault();

            const otp =
                document.getElementById("otp").value;

            const token =
                localStorage.getItem("access_token");

            const message =
                document.getElementById("message");

            try {

                const response = await fetch(
                    `${API_BASE}/verify-2fa?otp=${otp}`,
                    {
                        method: "POST",

                        headers: {
                            "Authorization":
                                `Bearer ${token}`
                        }
                    }
                );

                const data =
                    await response.json();

                if (response.ok) {

                    message.style.color =
                        "lightgreen";

                    message.innerText =
                        "2FA verification successful";

                    setTimeout(() => {

                        window.location.href =
                            "dashboard.html";

                    }, 1500);

                } else {

                    message.style.color =
                        "red";

                    message.innerText =
                        data.detail || "OTP verification failed";
                }

            } catch (error) {

                message.style.color =
                    "red";

                message.innerText =
                    "Server connection failed";
            }
        }
    );
}