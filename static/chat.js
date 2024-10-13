document.addEventListener('DOMContentLoaded', () => {
    // Function to scroll the chat window to the bottom
    function scrollToBottom() {
        const chatWindow = document.getElementById('chat-window');
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Call scrollToBottom after the page loads
    scrollToBottom();

    const chatForm = document.querySelector('.chat-form');

    handleAjaxFormSubmit(chatForm, {
        onSuccess: function (data, context) {
            const { submitter } = context;

            if (data.success) {
                // Handle goodbye (if the chat has ended)
                if (data.goodbye) {
                    window.location.href = '/story-hub'; // Redirect to another page
                    return;
                }

                // Update the chat window with the new messages
                const chatWindow = document.getElementById('chat-window');
                data.messages.forEach(function (message) {
                    const messageElement = createMessageElement(message);
                    chatWindow.appendChild(messageElement);
                });

                // Re-initialize event listeners for audio playback and text formatting
                initAudioPlayback();
                formatMessageTexts();

                // Scroll to bottom
                scrollToBottom();

                // Clear the input field if action was Send
                if (submitter && submitter.value === 'Send') {
                    document.getElementById('user-input').value = '';
                }

            } else {
                // Handle error
                alert('Error: ' + data.error);
            }
        },
        onError: function (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred.');
        }
    });

    function createMessageElement(message) {
        // Create DOM elements to represent the message
        // Based on the existing HTML structure
        const messageDiv = document.createElement('div');

        // For ambient messages
        if (message.alignment === 'center') {
            messageDiv.className = 'ambient-message';
            messageDiv.setAttribute('data-file-url', message.file_url);

            const messageTextDiv = document.createElement('div');
            messageTextDiv.className = 'ambient-message-text message-text';
            messageTextDiv.innerHTML = message.message_text; // Use innerHTML to allow HTML formatting

            const playIcon = document.createElement('i');
            playIcon.className = 'fas play-icon';

            messageDiv.appendChild(messageTextDiv);
            messageDiv.appendChild(playIcon);

        } else {
            // For chat bubbles
            messageDiv.className = 'chat-bubble ' + message.alignment;
            messageDiv.setAttribute('data-file-url', message.file_url);

            const avatarImg = document.createElement('img');
            avatarImg.alt = message.sender_name;
            avatarImg.className = 'avatar';
            avatarImg.src = message.sender_photo_url;

            const messageContentDiv = document.createElement('div');
            messageContentDiv.className = 'message-content';

            const senderLabelDiv = document.createElement('div');
            senderLabelDiv.className = 'sender-label';
            senderLabelDiv.innerText = message.sender_name;

            const messageTextDiv = document.createElement('div');
            messageTextDiv.className = 'message-text';
            messageTextDiv.innerHTML = message.message_text; // Use innerHTML

            messageContentDiv.appendChild(senderLabelDiv);
            messageContentDiv.appendChild(messageTextDiv);

            const playIcon = document.createElement('i');
            playIcon.className = 'fas play-icon';

            messageDiv.appendChild(avatarImg);
            messageDiv.appendChild(messageContentDiv);
            messageDiv.appendChild(playIcon);
        }

        return messageDiv;
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

    // Existing code for message text formatting on page load
    formatMessageTexts();
});