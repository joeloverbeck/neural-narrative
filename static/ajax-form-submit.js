// static/ajax-form-submit.js

// Utility function to display messages
function displayMessage(messageDiv, message, type) {
    if (messageDiv) {
        messageDiv.innerHTML = '<p>' + message + '</p>';
        messageDiv.classList.remove('success', 'error');
        messageDiv.classList.add(type);
        messageDiv.style.display = 'block'; // Ensure it's visible
    } else {
        alert((type === 'error' ? 'Error: ' : '') + message);
    }
}

function updateGrid(containerSelector, items, createItemElement) {
    var grid = document.querySelector(containerSelector);
    if (!grid) return;

    items.forEach(function(item) {
        var element = createItemElement(item);
        grid.appendChild(element);
    });
}

// Main function to handle AJAX form submissions
function handleAjaxFormSubmit(form, options = {}) {
    const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
    const originalButtonHTMLs = [];
    let clickedButton = null;

    // Find the message div
    const messageSelector = form.getAttribute('data-message-selector');
    const messageDiv = messageSelector ? document.querySelector(messageSelector) : form.parentElement.querySelector('.ajax-message');

    // Track which submit button was clicked
    submitButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            clickedButton = event.target;
        });
    });

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent traditional form submission

        if (typeof options.beforeSend === 'function') {
            options.beforeSend({ submitter: clickedButton });
        }

        submitButtons.forEach((button, index) => {
            originalButtonHTMLs[index] = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        });

        const formData = new FormData(form);

        if (clickedButton && clickedButton.name) {
            formData.append(clickedButton.name, clickedButton.value);
        }

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok (${response.status})`);
                }
                return response.json();
            })
            .then((data) => {
                if (typeof options.onSuccess === 'function') {
                    options.onSuccess(data, { submitter: clickedButton, messageDiv, form });
                } else {
                    // Default success handling
                    if (data.success) {
                        displayMessage(messageDiv, data.message || 'Success', 'success');
                    } else {
                        displayMessage(messageDiv, data.error || 'An error occurred', 'error');
                    }
                }
            })
            .catch((error) => {
                if (typeof options.onError === 'function') {
                    options.onError(error, { messageDiv, form });
                } else {
                    // Default error handling
                    console.error('Error:', error);
                    displayMessage(messageDiv, 'An unexpected error occurred.', 'error');
                }
            })
            .finally(() => {
                submitButtons.forEach((button, index) => {
                    button.disabled = false;
                    button.innerHTML = originalButtonHTMLs[index];
                });
                if (typeof options.onFinally === 'function') {
                    options.onFinally();
                }
            });
    });
}
