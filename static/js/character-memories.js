// static/character-memories.js

function insertMemorySuccessHandler(data, context) {
    if (data.success) {
        showToast(data.message || 'Memory saved successfully', 'success');

        // Ensure the context and form are available
        if (context && context.form) {
            // Select the textarea with the name "character_memory" within the form
            const textarea = context.form.querySelector('textarea[name="character_memory"]');

            // If the textarea exists, clear its content
            if (textarea) {
                textarea.value = '';
            }
        } else {
            // Fallback: Select the textarea by its ID if context is not available
            const textarea = document.getElementById('character_memory');
            if (textarea) {
                textarea.value = '';
            }
        }
    } else {
        showToast(data.error || 'An error occurred', 'error');
    }
}

function resolveWorldviewSuccess(data, context){
    if (data.success) {
        showToast(data.message || 'Worldview generated successfully.', 'success');

        // Update the worldview-container
        const container = document.getElementById('worldview-container');
        if (container) {
            // Update the content with the worldview_text
            container.innerHTML = `
                <p>${data.worldview_text}</p>`;
            }
    } else {
        showToast(data.error || 'An error occurred while generating worldview.', 'error');
    }
}

function resolveSelfReflectionSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Self-reflection generated successfully.', 'success');

        // Update the self-reflection-container
        const container = document.getElementById('self-reflection-container');
        if (container) {
            // Update the content with the self_reflection_text
            container.innerHTML = `<p>${data.self_reflection_text}</p>`;
            }
    } else {
        showToast(data.error || 'An error occurred while generating self-reflection.', 'error');
    }
}

