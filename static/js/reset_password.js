document.addEventListener('DOMContentLoaded',function (){
    'use strict'
    const new_password = document.getElementById("new-password")
    const confirm_password = document.getElementById("confirm-password")
    const togglePassword = document.getElementById("togglePassword");
    const togglePasswordConfirm = document.getElementById("togglePasswordConfirm");
    const passwordError = document.getElementById("passwordError");
    const confirmPasswordError = document.getElementById("confirmPasswordError");
    const form = document.getElementById("reset-password-form")
    let newPasswordValid=false;
    let confirmPasswordValid=false;
    
    togglePassword.addEventListener('click', function () {
        const type = new_password.getAttribute('type') === 'password' ? 'text' : 'password';
        new_password.setAttribute('type', type);
        this.querySelector('i').classList.toggle('bi-eye');
        this.querySelector('i').classList.toggle('bi-eye-slash');
    });
    
    togglePasswordConfirm.addEventListener('click', function () {
        const type = confirm_password.getAttribute('type') === 'password' ? 'text' : 'password';
        confirm_password.setAttribute('type', type);
        this.querySelector('i').classList.toggle('bi-eye');
        this.querySelector('i').classList.toggle('bi-eye-slash');
    });

    function validateNewPassword(){
        const passwordRegex = /^.{8,}$/;
        if (!passwordRegex.test(new_password.value)){
            passwordError.textContent = "La contraseña debe tener al menos 8 caracteres";
            newPasswordValid=false;
        }else{
            passwordError.textContent="";
            newPasswordValid=true;
        }
    }
    
    function validateConfirmPassword(){
        const passwordRegex = /^.{8,}$/;
        if (!passwordRegex.test(confirm_password.value)){
            confirmPasswordError.textContent = "La contraseña debe tener al menos 8 caracteres";
            confirmPasswordValid=false;
        }else if(new_password.value!=confirm_password.value){
            confirmPasswordError.textContent="Las contraseñas no coinciden";
            confirmPasswordValid=false;
        }else{
            confirmPasswordError.textContent="";
            confirmPasswordValid=true;
        }
    }

    new_password.addEventListener("keyup",validateNewPassword);
    confirm_password.addEventListener("keyup",validateConfirmPassword);

    form.addEventListener("submit", function(event){
        if (!(newPasswordValid && confirmPasswordValid)) {
            event.preventDefault();
            event.stopPropagation();
        }
    },false)
});
