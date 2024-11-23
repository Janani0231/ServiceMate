// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const password = form.querySelector('input[type="password"]');
            if (password && password.value.length < 8) {
                event.preventDefault();
                alert('Password must be at least 8 characters long');
            }
        });
    }
    
    // Dynamic form fields based on user type
    const userTypeSelect = document.querySelector('select[name="user_type"]');
    if (userTypeSelect) {
        const customerFields = document.querySelectorAll('.customer-field');
        const professionalFields = document.querySelectorAll('.professional-field');
        
        userTypeSelect.addEventListener('change', function() {
            if (this.value === 'customer') {
                customerFields.forEach(field => field.style.display = 'block');
                professionalFields.forEach(field => field.style.display = 'none');
            } else {
                customerFields.forEach(field => field.style.display = 'none');
                professionalFields.forEach(field => field.style.display = 'block');
            }
        });
    }
});