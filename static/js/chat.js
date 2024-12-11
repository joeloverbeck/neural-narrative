// static/chat.js

// Function to append messages to the chat window
function appendMessages(messages) {
    messages.forEach(function(message) {
        let messageHtml = '';
        if (message.alignment === 'center') {
            if (message.message_type === 'ambient') {
                messageHtml = `
                <div class="ambient-message" data-file-url="${message.file_url}">
                    <div class="ambient-message-text">${message.message_text}</div>
                    <i class="fas fa-play play-icon"></i>
                    <div class="waveform">
                        <div></div><div></div><div></div><div></div><div></div>
                    </div>
                </div>`;
            }
            else if (message.message_type === 'narrative_beat'){
                messageHtml = `
                <div class="narrative-beat-message" data-file-url="${message.file_url}">
                    <div class="narrative-beat-message-text">${message.message_text}</div>
                    <i class="fas fa-play play-icon"></i>
                    <div class="waveform">
                        <div></div><div></div><div></div><div></div><div></div>
                    </div>
                </div>`;
            } else if (message.message_type === 'confrontation_round') {
                messageHtml = `
                <div class="confrontation-round-message" data-file-url="${message.file_url}">
                    <div class="confrontation-round-message-text">${message.message_text}</div>
                    <i class="fas fa-play play-icon"></i>
                    <div class="waveform">
                        <div></div><div></div><div></div><div></div><div></div>
                    </div>
                </div>`;
            }
            else if (message.message_type === 'event') {
                messageHtml = `
                <div class="event-message" data-file-url="${message.file_url}">
                    <div class="event-message-text">${message.message_text}</div>
                    <i class="fas fa-play play-icon"></i>
                    <div class="waveform">
                        <div></div><div></div><div></div><div></div><div></div>
                    </div>
                </div>`;
            }
        } else {
            messageHtml = `
            <div class="chat-bubble ${message.alignment}" data-file-url="${message.file_url}">
                <img alt="${message.sender_name}" class="avatar" src="${message.sender_photo_url}">
                <div class="message-content">
                    <div class="sender-label">${message.sender_name}</div>
                    <div class="message-text">${message.message_text} ${message.desired_action}</div>
                </div>
                <i class="fas fa-play play-icon"></i>
                <div class="waveform">
                    <div></div><div></div><div></div><div></div><div></div>
                </div>
            </div>`;
        }
        $('#chat-window').append(messageHtml);
    });

    formatMessageTexts();
}

function formatMessageTexts() {
    var messageTexts = document.querySelectorAll('.message-text');

    messageTexts.forEach(function (messageText) {
        var content = messageText.innerHTML;

        var updatedContent = content.replace(/^\*(.*?)\*\s*(.*)/, '<span class="narration">$1</span><div class="narration-break"></div>$2');

        updatedContent = updatedContent.replace(/\*(.*?)\*/g, '<span class="narration">$1</span>');

        messageText.innerHTML = updatedContent;
    });
}

function brainstormEventsSuccessHandler(response) {
    if (response.success) {
        const container = document.getElementById('brainstormed-events-container');
        if (container) {
            if (response.brainstormed_events.length === 0) {
                container.innerHTML = '<p>No events were brainstormed.</p>';
            } else {
                // Clear previous events
                container.innerHTML = '';

                // Create a header for the brainstormed events
                const header = document.createElement('h3');
                header.textContent = 'Brainstormed Events';
                container.appendChild(header);

                // Create a list to display events
                const eventsList = document.createElement('ul');
                eventsList.classList.add('brainstormed-events-list');

                response.brainstormed_events.forEach((eventText, index) => {
                    const listItem = document.createElement('li');
                    listItem.textContent = eventText;
                    eventsList.appendChild(listItem);
                });

                container.appendChild(eventsList);
            }
        }
    } else {
        showToast(response.error || 'An error occurred while brainstorming events.', 'error');
    }
}

// Function to handle AJAX success for both chat and event forms
function chatSuccessHandler(response) {
    if (response.goodbye){
        // Handle goodbye scenario
        window.location.href = '/story-hub';
    }
    else if (response.success) {
        // Update the chat window with new messages
        appendMessages(response.messages);
        // Clear the input fields
        $('#user-input').val('');
        $('#event-input').val('');
        // Scroll to the bottom
        $('#chat-window').scrollTop($('#chat-window')[0].scrollHeight);
    } else {
        showToast(response.error || 'error',  'error');
    }
}

// Function to handle AJAX errors
function chatErrorHandler(xhr, status, error) {
    showToast(xhr || error, 'error');
}


function addParticipantsSuccessHandler(response) {
    if (response.success) {
        showToast(response.message || 'Participants added successfully.', 'success');
        // Optionally, reload the page to update the participants
        location.reload();
    } else {
        showToast(response.error || 'An error occurred while adding participants.', 'error');
    }
}

function removeParticipantsSuccessHandler(response) {
    if (response.success) {
        showToast(response.message || 'Participants removed successfully.', 'success');
        // Optionally, reload the page to update the participants
        location.reload();
    } else {
        showToast(response.error || 'An error occurred while removing participants.', 'error');
    }
}

// Function to scroll the chat window to the bottom
function scrollToBottom() {
    const chatWindow = document.getElementById('chat-window');
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function pageInit(){
    // Call scrollToBottom after the page loads
    scrollToBottom();

    // Existing code for message text formatting on page load
    formatMessageTexts();
}
