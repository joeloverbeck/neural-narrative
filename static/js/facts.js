// static/facts.js


function insertFactSuccessHandler(data, context) {
    if (data.success) {
        showToast(data.message || 'Fact saved successfully', 'success');

        // Ensure the context and form are available
        if (context && context.form) {
            // Select the textarea with the name "fact" within the form
            const textarea = context.form.querySelector('textarea[name="fact"]');

            // If the textarea exists, clear its content
            if (textarea) {
                textarea.value = '';
            }
        } else {
            // Fallback: Select the textarea by its ID if context is not available
            const textarea = document.getElementById('fact');
            if (textarea) {
                textarea.value = '';
            }
        }
    } else {
        showToast(data.error || 'An error occurred', 'error');
    }
}

