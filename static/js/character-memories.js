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