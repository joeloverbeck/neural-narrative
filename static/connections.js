// static/connections.js

// Custom onSuccess handler for connection generation form
function connectionGenerationSuccess(data, context) {
    const { messageDiv } = context;
    if (data.success) {
        displayMessage(messageDiv, data.message || 'Success', 'success');
    } else {
        displayMessage(messageDiv, data.error || 'An error occurred', 'error');
    }
}

// Initialize forms with custom onSuccess handler
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form.ajax-form');

    forms.forEach((form) => {
        handleAjaxFormSubmit(form, {
            onSuccess: connectionGenerationSuccess,
        });
    });
});