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

function createWaveformDiv(){
    const waveformDiv = document.createElement('div');
    waveformDiv.className = 'waveform';

    for (let i = 0; i < 5; i++) {
        waveformDiv.appendChild(document.createElement('div'));
    }
    
    return waveformDiv;
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

function createNarrationOutcomeDiv(sectionTitle, textContent, voiceLineUrl) {
    const sectionDiv = document.createElement('div');
    sectionDiv.classList.add(sectionTitle.toLowerCase());
    sectionDiv.setAttribute('data-file-url', voiceLineUrl || '');

    const h3 = document.createElement('h3');
    h3.textContent = sectionTitle;

    const p = document.createElement('p');
    p.textContent = textContent;

    const playIcon = document.createElement('i');
    playIcon.classList.add('fas', 'fa-play', 'play-icon');

    const waveformDiv = createWaveformDiv();

    sectionDiv.append(h3, p, playIcon, waveformDiv);

    return sectionDiv;
}

function createActionResultDiv(dataResult) {
    const actionResultDiv = document.createElement('div');
    actionResultDiv.classList.add('action-result');

    const narrationDiv = createNarrationOutcomeDiv(
        'Narration',
        dataResult.narrative,
        dataResult.narrative_voice_line_url
    );
    const outcomeDiv = createNarrationOutcomeDiv(
        'Outcome',
        dataResult.outcome,
        dataResult.outcome_voice_line_url
    );

    actionResultDiv.append(narrationDiv, outcomeDiv);

    return actionResultDiv;
}

function createCharacterModificationForm(characters, formAction) {
    const form = document.createElement('form');
    form.action = formAction || '';
    form.method = 'post';
    form.classList.add('ajax-form');
    form.dataset.successHandler = 'modifyCharactersSuccess';

    const inputFormType = document.createElement('input');
    inputFormType.type = 'hidden';
    inputFormType.name = 'form_type';
    inputFormType.value = 'modify_characters';
    form.appendChild(inputFormType);

    characters.forEach((character) => {
        const characterDiv = document.createElement('div');
        characterDiv.classList.add('character-modification');

        const h3 = document.createElement('h3');
        h3.textContent = character.name;

        const fields = [
            { label: 'Description:', key: 'description', value: character.description },
            { label: 'Equipment:', key: 'equipment', value: character.equipment },
            { label: 'Health:', key: 'health', value: character.health },
        ];

        characterDiv.appendChild(h3);

        fields.forEach((field) => {
            const id = `${field.key}_${character.identifier}`;
            const label = document.createElement('label');
            label.setAttribute('for', id);
            label.textContent = field.label;

            const textarea = document.createElement('textarea');
            textarea.id = id;
            textarea.name = id;
            textarea.textContent = field.value;

            characterDiv.append(label, textarea);
        });

        form.appendChild(characterDiv);
    });

    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.classList.add('action-button');

    const saveIcon = document.createElement('i');
    saveIcon.classList.add('fas', 'fa-save');
    submitButton.append(saveIcon, document.createTextNode(' Save Changes'));

    form.appendChild(submitButton);

    // Initialize the AJAX form submission
    handleAjaxFormSubmit(form, {
        onSuccess: window['modifyCharactersSuccess'],
    });

    return form;
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