document.addEventListener("DOMContentLoaded", function () {
    // Scroll to Top functionality.
    // Shows a "scroll to top" button when the user scrolls down more than 300px.
    // Smoothly scrolls to the top when the button is clicked.
    const scrollBtn = document.querySelector(".scroll-to-top");
    if (scrollBtn) {
        window.addEventListener("scroll", function () {
            if (window.pageYOffset > 300) {
                scrollBtn.classList.add("show");
            } else {
                scrollBtn.classList.remove("show");
            }
        });

        scrollBtn.addEventListener("click", function (e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: "smooth",
            });
        });
    }

    // Auto-hide alerts.
    // Automatically closes Bootstrap alerts after 5 seconds.
    document.querySelectorAll(".alert").forEach((alert) => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form Validation and Submission.
    // Handles form validation and submission for login and registration forms.
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");

    function handleFormSubmit(form, validationRules) {
        if (!form) return;

        form.addEventListener("submit", function (e) {
            let isValid = true;
            const submitBtn = this.querySelector('button[type="submit"]');
            const loadingText = submitBtn.dataset.loadingText || "Processing...";
            const originalText = submitBtn.innerHTML;

            // Validate fields.
            const fields = this.querySelectorAll(".form-control");
            fields.forEach((field) => {
                const errorDiv = field.parentElement.querySelector(".error-message");
                if (!errorDiv) return;

                let errorMessage = "";

                // Required field validation.
                if (!field.value && validationRules.required) {
                    errorMessage = "This field is required";
                }

                // Field-specific validation.
                if (field.value && validationRules[field.name]) {
                    const rule = validationRules[field.name];
                    if (!rule.pattern.test(field.value)) {
                        errorMessage = rule.message;
                    }
                }

                if (errorMessage) {
                    errorDiv.textContent = errorMessage;
                    errorDiv.style.display = "block";
                    isValid = false;
                } else {
                    errorDiv.style.display = "none";
                }
            });

            if (!isValid) {
                e.preventDefault();
                return;
            }

            // Show loading state.
            submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>${loadingText}`;
            submitBtn.disabled = true;
        });
    }

    // Initialize forms with validation rules.
    // Defines validation rules for username, password, and email fields.
    const validationRules = {
        required: true,
        username: {
            pattern: /^.{3,}$/,
            message: "Username must be at least 3 characters long",
        },
        password: {
            pattern: /^.{6,}$/,
            message: "Password must be at least 6 characters long",
        },
        email: {
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            message: "Please enter a valid email address",
        },
    };

    // Apply validation rules to login and registration forms.
    handleFormSubmit(loginForm, validationRules);
    handleFormSubmit(registerForm, validationRules);

    // Initialize tooltips if Bootstrap is present.
    // Adds Bootstrap tooltips to elements with the `data-bs-toggle="tooltip"` attribute.
    if (typeof bootstrap !== "undefined") {
        var tooltipTriggerList = [].slice.call(
            document.querySelectorAll('[data-bs-toggle="tooltip"]')
        );
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});