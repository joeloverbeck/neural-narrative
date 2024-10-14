// static/main.js

let currentAudio = null; // Global variable to keep track of the current playing audio

function playAudio(fileUrl, element) {
    if (!fileUrl || fileUrl === 'None' || fileUrl === 'null') {
        showToast('The audio file is not available.', 'error');
        return;
    }

    // Reset the Audio object if the source has changed
    if (element.audio) {
        if (element.audio.src !== new URL(fileUrl, window.location.origin).href) {
            element.audio.pause();
            element.audio = null;
        }
    }

    // Create new Audio object if it doesn't exist
    if (!element.audio) {
        element.audio = new Audio(fileUrl);

        // Add event listeners to manage 'playing' state
        element.audio.addEventListener('playing', function() {
            element.classList.add('playing');
        });
        element.audio.addEventListener('pause', function() {
            element.classList.remove('playing');
        });
        element.audio.addEventListener('ended', function() {
            element.classList.remove('playing');
            // Optionally, set element.audio to null to reset
            // element.audio = null;
        });
        element.audio.onerror = function() {
            console.error('Error occurred while loading audio:', element.audio.error);
            showToast('The audio file could not be loaded.', 'error');
            element.audio = null;
        };
    }

    // Check if the audio is playing
    if (element.audio.paused) {
        // Pause any currently playing audio
        if (currentAudio && currentAudio !== element.audio) {
            currentAudio.pause();
        }
        // Play the audio
        element.audio.play().catch(function(error) {
            console.error('Error occurred while playing audio:', error);
            showToast('The audio file couldn\'t be played.', error);
        });
        // Set the current playing audio
        currentAudio = element.audio;
    } else {
        // Audio is playing, so pause it
        element.audio.pause();
        currentAudio = null;
    }
}

function initAudioPlayback() {
    // When clicking on any part of the page.
    document.addEventListener('click', function(event) {
        // Grab closest element to the click event that has '[data-file-url]'
        const element = event.target.closest('[data-file-url]');
        // If audio has been initialized for that element.
        if (element && !element.classList.contains('audio-initialized')) {
            // Add click listener to that element.
            element.addEventListener('click', function(event) {
                // Execute playAudio for that fileUrl
                const fileUrl = event.currentTarget.getAttribute('data-file-url');
                playAudio(fileUrl, event.currentTarget);
            });
            element.style.cursor = 'pointer';
            element.classList.add('audio-initialized');

            element.click()
        }
    });
}

function updateGrid(containerSelector, items, createItemElement) {
    var grid = document.querySelector(containerSelector);
    if (!grid) return;

    items.forEach(function(item) {
        var element = createItemElement(item);
        grid.appendChild(element);
    });
}

function showToast(message, type) {
    const container = document.querySelector('.toast-container');
    if (!container) return; // Exit if container not found

    const toast = document.createElement('div');
    toast.classList.add('toast', type);
    toast.innerText = message;
    container.appendChild(toast);

    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.classList.add('fade-out');
        toast.addEventListener('animationend', () => toast.remove());
    }, 5000);
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
                        showToast(messageDiv, data.message || 'Success', 'success');
                    } else {
                        showToast(messageDiv, data.error || 'An error occurred', 'error');
                    }
                }
            })
            .catch((error) => {
                if (typeof options.onError === 'function') {
                    options.onError(error, { messageDiv, form });
                } else {
                    // Default error handling
                    console.error('Error:', error);
                    showToast(messageDiv, 'An unexpected error occurred.', 'error');
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

function initCollapsibles(){
    // Collapsible sections
    const collapsibles = document.querySelectorAll('.collapsible');
    collapsibles.forEach(function(collapsible) {
        collapsible.addEventListener('click', function() {
            this.classList.toggle('active');
            const content = this.nextElementSibling;
            if (content.style.display === 'block') {
                content.style.display = 'none';
            } else {
                content.style.display = 'block';
            }
        });

        // On load: Display content for any collapsible that has 'active' class
        if (collapsible.classList.contains('active')) {
            const content = collapsible.nextElementSibling;
            content.style.display = 'block';
        }
    });
}

function replaceFlashes(){
    const flashes = document.querySelectorAll('.flashes li');
    flashes.forEach(flash => {
        const messageText = flash.innerText;
        const messageType = flash.classList.contains('success') ? 'success' : 'error';
        showToast(messageText, messageType);
    });

    // Optionally, remove the flash messages from the DOM
    const flashList = document.querySelector('.flashes');
    if (flashList) {
        flashList.remove();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Initialize audio playback elements on page load
    initAudioPlayback();

    // Initialize the collapsibles on page load
    initCollapsibles();

    replaceFlashes();

    // Initialize AJAX
    const forms = document.querySelectorAll('form.ajax-form');

    forms.forEach((form) => {
        const successHandlerName = form.dataset.successHandler;
        const successHandler = window[successHandlerName];

        const errorHandlerName = form.dataset.errorHandler;
        const errorHandler = window[errorHandlerName];

        handleAjaxFormSubmit(form, {
            onSuccess: successHandler,
            onError: errorHandler
        });
    });

    // Call page-specific initialization if it exists
    if (typeof pageInit === 'function') {
        pageInit();
    }
});