// static/interview.js

function sendIntervieweeResponseSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Response sent successfully', 'success');

        // Remove existing Skip Question button messages
        const existingSkipButtonMessages = document.querySelectorAll('.message.system .skip-question-button');
        existingSkipButtonMessages.forEach(button => {
            button.closest('.message').remove();
        });

        const messagesContainer = document.querySelector('.messages-container');
        if (messagesContainer) {
            // Add the new message
            const messageElement = createMessageElement(data.new_message);
            messagesContainer.appendChild(messageElement);

            // Scroll to the bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;

            // Remove the input form
            const formElement = context.form.parentElement.parentElement;
            if (formElement) {
                formElement.remove();
            }

            // Add the interviewer message with the generate question button
            const interviewerMessage = createInterviewerGenerateButtonMessage();
            messagesContainer.appendChild(interviewerMessage);
        }
    } else {
        showToast(data.error || 'An error occurred', 'error');
    }
}

function createMessageElement(messageData) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', messageData.role);

    const headerDiv = document.createElement('div');
    headerDiv.classList.add('message-header');

    const senderSpan = document.createElement('span');
    senderSpan.classList.add('message-sender');
    senderSpan.textContent = messageData.sender;

    const timeSpan = document.createElement('span');
    timeSpan.classList.add('message-time');
    timeSpan.textContent = messageData.timestamp || new Date().toLocaleTimeString();

    headerDiv.appendChild(senderSpan);
    headerDiv.appendChild(timeSpan);

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    contentDiv.innerHTML = messageData.content;

    messageDiv.appendChild(headerDiv);
    messageDiv.appendChild(contentDiv);

    return messageDiv;
}

function createSkipQuestionButtonMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'system'); // Use 'system' or another appropriate class

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');

    const skipButton = document.createElement('button');
    skipButton.classList.add('skip-question-button', 'action-button');
    skipButton.innerHTML = '<i class="fas fa-forward"></i> Skip Question';

    // Attach event handler to skipButton
    skipButton.addEventListener('click', function() {
        const interviewerMessages = document.querySelectorAll('.message.interviewer');
        const lastInterviewerMessage = interviewerMessages[interviewerMessages.length - 1];
        if (lastInterviewerMessage) {
            skipQuestion(lastInterviewerMessage);
        } else {
            console.error('No interviewer messages found.');
        }
    });

    contentDiv.appendChild(skipButton);
    messageDiv.appendChild(contentDiv);

    return messageDiv;
}

function createInterviewerGenerateButtonMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'interviewer');

    const headerDiv = document.createElement('div');
    headerDiv.classList.add('message-header');

    const senderSpan = document.createElement('span');
    senderSpan.classList.add('message-sender');
    senderSpan.textContent = 'Interviewer';

    headerDiv.appendChild(senderSpan);

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');

    const button = document.createElement('button');
    button.classList.add('generate-question-button', 'action-button');
    button.innerHTML = '<i class="fas fa-question-circle"></i> Generate Next Question';

    // Set data-character-identifier attribute
    button.setAttribute('data-character-identifier', document.querySelector('#character_selector').value);

    button.addEventListener('click', generateNextQuestion);

    contentDiv.appendChild(button);

    messageDiv.appendChild(headerDiv);
    messageDiv.appendChild(contentDiv);

    return messageDiv;
}

function remove_previous_skip_buttons() {
    const previousInterviewerMessages = document.querySelectorAll('.message.interviewer');

    previousInterviewerMessages.forEach(message => {
        if (message !== newMessageElement) {
            const skipButton = message.querySelector('.skip-question-button');
            if (skipButton) {
                skipButton.remove();
            }
        }
    });
}

function skipQuestion(messageDiv) {
    const characterIdentifier = document.querySelector('#character_selector').value;
    const formData = new FormData();
    formData.append('submit_action', 'skip_question');
    formData.append('character_identifier', characterIdentifier);

    fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message || 'Question skipped', 'success');

            // Replace the interviewer message with the new message
            const newMessageElement = createMessageElement(data.new_message);
            messageDiv.parentNode.replaceChild(newMessageElement, messageDiv);

            const messagesContainer = document.querySelector('.messages-container');

            // Remove existing Skip Question button messages
            const existingSkipButtonMessages = document.querySelectorAll('.message.system .skip-question-button');
            existingSkipButtonMessages.forEach(button => {
                button.closest('.message').remove();
            });

            // Add the new Skip Question button message immediately after the latest interviewer message
            const skipButtonMessage = createSkipQuestionButtonMessage();
            const interviewerMessages = document.querySelectorAll('.message.interviewer');
            const lastInterviewerMessage = interviewerMessages[interviewerMessages.length - 1];

            if (lastInterviewerMessage) {
                lastInterviewerMessage.parentNode.insertBefore(skipButtonMessage, lastInterviewerMessage.nextSibling);
            } else {
                messagesContainer.appendChild(skipButtonMessage);
            }

            // Scroll to the bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        } else {
            showToast(data.error || 'An error occurred', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An unexpected error occurred.', 'error');
    });
}

function generateNextQuestion() {
    const characterIdentifier = document.querySelector('#character_selector').value;
    const formData = new FormData();
    formData.append('submit_action', 'generate_next_question');
    formData.append('character_identifier', characterIdentifier);

    fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message || 'Question generated', 'success');

            const messagesContainer = document.querySelector('.messages-container');
            if (messagesContainer) {
                // Remove the generate question button message
                const buttonMessage = document.querySelector('.message.interviewer .generate-question-button')?.closest('.message');
                if (buttonMessage) {
                    buttonMessage.remove();
                }

                // Add the new interviewer message
                const messageElement = createMessageElement(data.new_message);
                messagesContainer.appendChild(messageElement);

                // Remove existing Skip Question button messages
                const existingSkipButtonMessages = document.querySelectorAll('.message.system .skip-question-button');
                existingSkipButtonMessages.forEach(button => {
                    button.closest('.message').remove();
                });

                // Add the Skip Question button message
                const skipButtonMessage = createSkipQuestionButtonMessage();
                messagesContainer.appendChild(skipButtonMessage);

                // Scroll to the bottom
                messagesContainer.scrollTop = messagesContainer.scrollHeight;

                // Add the interviewee input form
                const intervieweeMessage = createIntervieweeInputMessage();
                messagesContainer.appendChild(intervieweeMessage);
            }
        } else {
            showToast(data.error || 'An error occurred', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An unexpected error occurred.', 'error');
    });
}

function createIntervieweeInputMessage() {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'interviewee');

    const headerDiv = document.createElement('div');
    headerDiv.classList.add('message-header');

    const senderSpan = document.createElement('span');
    senderSpan.classList.add('message-sender');

    // Get the selected character's name
    const characterName = document.querySelector('#character_selector option:checked').textContent;
    senderSpan.textContent = characterName;

    headerDiv.appendChild(senderSpan);

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');

    const form = document.createElement('form');
    form.method = 'post';
    form.classList.add('ajax-form');
    form.dataset.successHandler = 'sendIntervieweeResponseSuccess';

    const characterIdentifierInput = document.createElement('input');
    characterIdentifierInput.type = 'hidden';
    characterIdentifierInput.name = 'character_identifier';
    characterIdentifierInput.value = document.querySelector('#character_selector').value;

    const textarea = document.createElement('textarea');
    textarea.name = 'interviewee_response';
    textarea.rows = 3;
    textarea.placeholder = 'Enter your response...';

    const sendButton = document.createElement('button');
    sendButton.type = 'submit';
    sendButton.name = 'submit_action';
    sendButton.value = 'send_interviewee_response';
    sendButton.classList.add('action-button');
    sendButton.innerHTML = '<i class="fas fa-paper-plane"></i> Send Response';

    const generateButton = document.createElement('button');
    generateButton.type = 'submit';
    generateButton.name = 'submit_action';
    generateButton.value = 'generate_interviewee_response';
    generateButton.classList.add('action-button');
    generateButton.innerHTML = '<i class="fas fa-magic"></i> Generate Response';

    // Create a container for buttons to apply flex properties
    const buttonContainer = document.createElement('div');
    buttonContainer.style.display = 'flex';
    buttonContainer.style.gap = '5px'; // Adjust the gap as needed
    buttonContainer.style.justifyContent = 'center';

    buttonContainer.appendChild(sendButton);
    buttonContainer.appendChild(generateButton);

    form.appendChild(characterIdentifierInput);
    form.appendChild(textarea);
    form.appendChild(buttonContainer);

    contentDiv.appendChild(form);

    messageDiv.appendChild(headerDiv);
    messageDiv.appendChild(contentDiv);

    // Initialize AJAX form submission
    handleAjaxFormSubmit(form, {
        onSuccess: sendIntervieweeResponseSuccess,
    });

    return messageDiv;
}

// On page load
document.addEventListener('DOMContentLoaded', () => {
    // Add event listener to generate question button if present
    const generateQuestionButton = document.querySelector('.generate-question-button');
    if (generateQuestionButton) {
        generateQuestionButton.addEventListener('click', generateNextQuestion);
    }
});