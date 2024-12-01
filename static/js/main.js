// static/js/main.js

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
            showToast('The audio file couldn\'t be played. Error: ' + error, 'error');
        });
        // Set the current playing audio
        currentAudio = element.audio;
    } else {
        // Audio is playing, so pause it
        element.audio.pause();
        currentAudio = null;
    }
}

function delayedRedirect(url){
    setTimeout(() => {
        window.location.href = url;
    }, 4000); // Redirects after 4 seconds
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

function createWaveformDiv(){
    const waveformDiv = document.createElement('div');
    waveformDiv.className = 'waveform';

    for (let i = 0; i < 5; i++) {
        waveformDiv.appendChild(document.createElement('div'));
    }
    
    return waveformDiv;
}

/* Handling results of a query to the database */
function queryDatabaseSuccessHandler(data, context) {
    if (data.success) {
        showToast(data.message || 'Query successful', 'success');

        const resultsDiv = document.getElementById('query-results');
        if (resultsDiv) {
            // Clear previous results
            resultsDiv.innerHTML = '';

            // Check if data.results is an array
            if (Array.isArray(data.results) && data.results.length > 0) {
                const ul = document.createElement('ul');
                ul.className = 'query-list';

                data.results.forEach((result, index) => {
                    const li = document.createElement('li');
                    li.style.setProperty('--i', index);

                    const icon = document.createElement('i');
                    icon.className = 'fas fa-book-open'; // Choose an appropriate icon
                    icon.style.marginRight = '15px';

                    const text = document.createElement('span');
                    text.textContent = 'ID(' + result['id']  + '): ' + result['document'];

                    li.appendChild(icon);
                    li.appendChild(text);
                    ul.appendChild(li);
                });
                resultsDiv.appendChild(ul);
            } else {
                resultsDiv.textContent = 'No results found.';
            }
        }
    } else {
        showToast(data.error || 'An error occurred', 'error');
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
    }, 10000);
}

// Variable to store the value of the clicked submit button
var submitActionValue = null;

// Capture the click event on submit buttons
$('form.ajax-form button[type=submit]').click(function() {
  submitActionValue = $(this).val();
});

function disable_button_and_add_spinner(button) {
    button.disabled = true;

    if (button.classList.contains('icon-button')) {
        // For icon buttons, show only the spinner icon
        button.innerHTML = '<i class="fa-solid fa-arrows-rotate fa-spin"></i>';
    } else {
        // For other buttons, show the spinner icon with "Processing..." text
        button.innerHTML = '<i class="fa-solid fa-arrows-rotate fa-spin"></i> Processing...';
    }
}

// Main function to handle AJAX form submissions
function handleAjaxFormSubmit(form, options = {}) {
    const submitButtons = form.querySelectorAll('button[type="submit"], input[type="submit"]');
    const originalButtonHTMLs = [];
    let clickedButton = null;

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
            disable_button_and_add_spinner(button);
        });

        const formData = new FormData(form);

        if (clickedButton && clickedButton.name) {
            formData.append(clickedButton.name, clickedButton.value);
        }

          // Include the submit_action parameter
          if (submitActionValue !== null) {
            formData.append('submit_action', submitActionValue);
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
                    options.onSuccess(data, { submitter: clickedButton, form });
                } else {
                    // Default success handling
                    if (data.success) {
                        showToast(data.message || 'Success', 'success');
                    } else {
                        showToast(data.error || 'An error occurred', 'error');
                    }
                }
            })
            .catch((error) => {
                if (typeof options.onError === 'function') {
                    options.onError(error, { form });
                } else {
                    // Default error handling
                    console.error('Error:', error);
                    showToast('An unexpected error occurred.', 'error');
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
            const content = this.nextElementSibling;
            if (content.style.display === 'block') {
                this.classList.remove('active');
                content.style.display = 'none';
            } else {
                this.classList.add('active');
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

function createCollapsibleSection(title, iconClass, contentElement, isActive = false) {
    const collapsibleSection = document.createElement('div');
    collapsibleSection.classList.add('collapsible-section');

    const collapsibleButton = document.createElement('button');
    collapsibleButton.classList.add('collapsible');
    if (isActive) {
        collapsibleButton.classList.add('active');
    }
    const icon = document.createElement('i');
    icon.classList.add('fas', iconClass);
    collapsibleButton.appendChild(icon);
    collapsibleButton.appendChild(document.createTextNode(` ${title}`));

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('content');
    if (isActive) {
        contentDiv.style.display = 'block';
    }

    contentDiv.appendChild(contentElement);

    collapsibleSection.appendChild(collapsibleButton);
    collapsibleSection.appendChild(contentDiv);

    // Initialize the collapsible behavior
    collapsibleButton.addEventListener('click', function () {
        this.classList.toggle('active');
        contentDiv.style.display = contentDiv.style.display === 'block' ? 'none' : 'block';
    });

    return collapsibleSection;
}

function updateDescription(type) {
    // Construct the select element's ID based on the type
    const selectId = `${type}_name`;
    const select = document.getElementById(selectId);

    // Ensure the select element exists
    if (!select) {
        console.warn(`Select element with ID "${selectId}" not found.`);
        return;
    }

    const descriptionElement = document.getElementById(`${type}_description`)?.querySelector('p');

    // Ensure the description element exists
    if (!descriptionElement) {
        console.warn(`Description element for type "${type}" not found.`);
        return;
    }

    // Check if the select has any options
    if (select.options.length === 0) {
        // Handle the case when there are no options
        descriptionElement.innerText = 'No description available.';
        return;
    }

    // Get the currently selected option
    const selectedIndex = select.selectedIndex;

    // Ensure a valid option is selected
    if (selectedIndex === -1) {
        // No option is selected; possibly set a default description
        descriptionElement.innerText = 'No item selected.';
        return;
    }

    const selectedOption = select.options[selectedIndex];

    // Retrieve the 'data-description' attribute from the selected option
    const description = selectedOption.getAttribute('data-description');

    // Set the description text, fallback to a default message if not available
    descriptionElement.innerText = description || 'No description provided for the selected item.';
}

function moveCursorToEnd(element) {
    // For modern browsers
    if (typeof element.setSelectionRange === "function") {
        // Ensure the element is focused
        element.focus();
        // Move cursor to the end
        const length = element.value.length;
        element.setSelectionRange(length, length);
    } else if (typeof element.createTextRange !== "undefined") { // For older IE
        element.focus();
        const range = element.createTextRange();
        range.collapse(false);
        range.select();
    }
}

function commonInitializations(){
    // Initialize audio playback elements on page load
    initAudioPlayback();

    // Initialize the collapsibles on page load
    initCollapsibles();

    replaceFlashes();
}

function initInputCursor() {
    const textInputs = document.querySelectorAll('input[type="text"]');
    textInputs.forEach(function(input) {
        input.addEventListener('focus', function() {
            setTimeout(() => {
                moveCursorToEnd(this);
            }, 0);
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    commonInitializations();

    // Initialize AJAX
    const forms = document.querySelectorAll('form.ajax-form');

    forms.forEach((form) => {
        const successHandlerName = form.dataset.successHandler;
        const successHandler = window[successHandlerName];

        const errorHandlerName = form.dataset.errorHandler;
        const errorHandler = window[errorHandlerName];

        if (successHandler) {
            handleAjaxFormSubmit(form, {
                onSuccess: successHandler,
                onError: errorHandler
            });
        }
    });

    // Initialize input cursor positioning
    initInputCursor();

    // Call page-specific initialization if it exists
    if (typeof pageInit === 'function') {
        pageInit();
    }
});