document.addEventListener('DOMContentLoaded', function() {
    console.log("register")
    'use strict';

    // Form validation and step navigation
    const form = document.getElementById('registrationForm');
    const step1 = document.getElementById('step-1');
    const step2 = document.getElementById('step-2');
    const nextStep = document.getElementById('nextStep');
    const prevStep = document.getElementById('prevStep');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const togglePassword = document.getElementById('togglePassword');
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
    const indicatorStep1 = document.getElementById('indicator-step-1');
    const indicatorStep2 = document.getElementById('indicator-step-2');
    const passwordError=document.getElementById('passwordError');
    const confirmPasswordError=document.getElementById('confirmPasswordError');
    let step1Valid = false;
    let step2Valid = false;

    // Toggle password visibility
    togglePassword.addEventListener('click', function() {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.querySelector('i').classList.toggle('bi-eye');
        this.querySelector('i').classList.toggle('bi-eye-slash');
    });

    toggleConfirmPassword.addEventListener('click', function() {
        const type = confirmPassword.getAttribute('type') === 'password' ? 'text' : 'password';
        confirmPassword.setAttribute('type', type);
        this.querySelector('i').classList.toggle('bi-eye');
        this.querySelector('i').classList.toggle('bi-eye-slash');
    });

    // Validate password match
    function validateStep1() {
        const passwordRegex = /^.{8,}$/;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        let passwordValid = false;
        let confirmPasswordValid = false;
        let emailValid = false;
        if (!emailRegex.test(email.value)) {
            email.classList.add('is-invalid');
            emailValid = false;
        }
        else {
            email.classList.remove('is-invalid');
            emailValid = true;
        }
        if (!passwordRegex.test(password.value)) {
            passwordError.textContent = "La contraseña debe tener al menos 8 caracteres";
            passwordValid = false;
        } else {
            passwordError.textContent = "";
            passwordValid = true;
        }
        if (password.value !== confirmPassword.value) {
            confirmPasswordError.textContent = "Las contraseñas no coinciden";
            confirmPasswordValid = false;
        } else {
            confirmPasswordError.textContent = "";
            confirmPasswordValid = true;
        }
        step1Valid = passwordValid && confirmPasswordValid && emailValid;
    }

    if (password && confirmPassword) {
        email.addEventListener("keyup", validateStep1);
        password.addEventListener("keyup", validateStep1);
        confirmPassword.addEventListener("keyup", validateStep1);
    }

    // Navigate to the next step
    nextStep.addEventListener('click', function() {
        validateStep1();
        if (step1Valid) {
            step1.classList.add('d-none');
            step2.classList.remove('d-none');
            indicatorStep1.classList.replace('bg-primary', 'bg-secondary');
            indicatorStep2.classList.replace('bg-secondary', 'bg-primary');
        }
    });

    // Navigate to the previous step
    prevStep.addEventListener('click', function() {
        step2.classList.add('d-none');
        step1.classList.remove('d-none');
        indicatorStep2.classList.replace('bg-primary', 'bg-secondary');
        indicatorStep1.classList.replace('bg-secondary', 'bg-primary');
    });

    // Form submission validation
    form.addEventListener('submit', function(event) {
        if (step2.querySelectorAll(':invalid').length > 0) {
            event.preventDefault();
            event.stopPropagation();
            step2.classList.add('was-validated');
        }
    });
});