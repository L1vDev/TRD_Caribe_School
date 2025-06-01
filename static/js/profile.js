document.addEventListener("DOMContentLoaded", function(){
    document.getElementById('profilePictureInput').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('profileImage').src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    document.getElementById('changePasswordButton').addEventListener('click', function () {
        const currentPassword = document.getElementById('currentPassword');
        const newPassword = document.getElementById('newPassword');
        const confirmPassword = document.getElementById('confirmPassword');
        let isValid = true;

        [currentPassword, newPassword, confirmPassword].forEach(field => {
            if (!field.value.trim()) {
                field.classList.add('is-invalid');
                isValid = false;
            } else {
                field.classList.remove('is-invalid');
            }
        });

        if (!isValid) return;

        if (newPassword.value !== confirmPassword.value) {
            alert('La nueva contraseña y la confirmación no coinciden.');
            return;
        }

        const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
        modal.hide();

        alert('Contraseña cambiada exitosamente.');
    });

    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const targetInput = document.getElementById(targetId);
            const icon = this.querySelector('i');

            if (targetInput.type === 'password') {
                targetInput.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            } else {
                targetInput.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    });
})