// static/interview.js

function sendIntervieweeResponseSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Response sent successfully', 'success');

        // Update the messages container
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

            // Update the messages container
            const messagesContainer = document.querySelector('.messages-container');
            if (messagesContainer) {
                // Remove the generate question button message
                const buttonMessage = document.querySelector('.message.interviewer .generate-question-button').closest('.message');
                if (buttonMessage) {
                    buttonMessage.remove();
                }

                // Add the new interviewer message
                const messageElement = createMessageElement(data.new_message);
                messagesContainer.appendChild(messageElement);

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

    const submitActionInput = document.createElement('input');
    submitActionInput.type = 'hidden';
    submitActionInput.name = 'submit_action';
    submitActionInput.value = 'send_interviewee_response';

    const textarea = document.createElement('textarea');
    textarea.name = 'interviewee_response';
    textarea.rows = 3;
    textarea.placeholder = 'Enter your response...';

    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.classList.add('action-button');
    submitButton.innerHTML = '<i class="fas fa-paper-plane"></i> Send Response';

    form.appendChild(characterIdentifierInput);
    form.appendChild(submitActionInput);
    form.appendChild(textarea);
    form.appendChild(submitButton);

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