// static/connections.js

// Custom onSuccess handler for connection generation form
function connectionGenerationSuccess(data, context) {
    const { messageDiv } = context;

    if (data.success) {
        showToast(data.message || 'Success', 'success');
    } else {
        showToast(data.error || 'An error occurred', 'error');
    }
}
