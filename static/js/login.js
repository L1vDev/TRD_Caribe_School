// Form validation script
document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  // Fetch all forms we want to apply validation styles to
  const form = document.getElementById('login-form');
  const togglePassword = document.getElementById('togglePassword');
  const forgotPassword= document.getElementById('forgotPasswordModal')
  const email=document.getElementById("email");

  email.addEventListener("keyup",()=>{
    const emailRegex= /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.value)) {
      email.classList.add('is-invalid');
      emailValid = false;
    }
    else {
        email.classList.remove('is-invalid');
        emailValid = true;
    } 
  });

  togglePassword.addEventListener('click', function () {
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.querySelector('i').classList.toggle('bi-eye');
    this.querySelector('i').classList.toggle('bi-eye-slash');
  });

  forgotPassword.addEventListener('shown.bs.modal', function () {
    document.getElementById('forgot-email').focus();
  });

  form.addEventListener('submit', function (event) {
    if (!form.checkValidity()) {
      event.preventDefault();
      event.stopPropagation();
      form.classList.add('was-validated');
    }
  }, false);

});