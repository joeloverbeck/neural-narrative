// static/character-generation.js

function fillGuideline(guideline) {
    document.getElementById('guideline_text').value = guideline;
}

function createGuidelineElement(guideline) {
    const postIt = document.createElement('div');
    postIt.classList.add('post-it', 'card');

    postIt.onclick = () => {
        fillGuideline(guideline);
    };

    const icon = document.createElement('i');
    icon.classList.add('fas', 'fa-thumbtack');
    postIt.appendChild(icon);

    const p = document.createElement('p');
    p.textContent = guideline;
    postIt.appendChild(p);

    postIt.classList.add('new-guideline');

    return postIt;
}

// Custom onSuccess handler for character generation forms
function characterGenerationSuccess(data, context) {
    const { messageDiv } = context;
    if (data.success) {
        displayMessage(messageDiv, data.message || 'Success', 'success');

        // If the response contains guidelines, update the grid
        if (data.guidelines) {
            updateGrid('.guidelines-grid', data.guidelines, createGuidelineElement);
        }
    } else {
        displayMessage(messageDiv, data.error || 'An error occurred', 'error');
    }
}

// Initialize forms with custom onSuccess handler
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form.ajax-form');

    forms.forEach((form) => {
        handleAjaxFormSubmit(form, {
            onSuccess: characterGenerationSuccess,
        });
    });
});