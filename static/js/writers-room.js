// static/js/writers-room.js

function writersRoomSuccess(data, context) {
    if (data.success) {
        if (data.action === 'end_session') {
            // Show success message
            showToast('Writers\' Room session ended successfully.', 'success');
            // Redirect after delay
            delayedRedirect(window.location.href);
        } else if (data.action === 'send') {
            const messagesContainer = document.querySelector('.messages-container');

            // Append the user's message
            const userMessage = document.getElementById('message-input').value;
            if (userMessage) {
                const userMessageData = {
                    message_text: userMessage,
                    message_type: 'user',
                };
                const userMessageElement = createMessageElement(userMessageData);
                messagesContainer.appendChild(userMessageElement);
            }

            // Append the responses
            data.messages.forEach(function(message) {
                const messageElement = createMessageElement(message);
                messagesContainer.appendChild(messageElement);
            });

            // Scroll to the bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;

            // Clear the input
            document.getElementById('message-input').value = '';
        }
    } else {
        showToast(data.error || 'An error occurred.', 'error');
    }
}

function createMessageElement(messageData) {
    const messageDiv = document.createElement('div');
    let formattedMessageType = messageData.message_type.toLowerCase().replace(/ /g, "_");

    messageDiv.classList.add('message', formattedMessageType);

    const headerDiv = document.createElement('div');
    headerDiv.classList.add('message-header');

    const senderSpan = document.createElement('span');
    senderSpan.classList.add('message-sender');
    senderSpan.textContent = messageData.message_type === 'user' ? 'You' : capitalizeFirstLetter(messageData.message_type);

    const timeSpan = document.createElement('span');
    timeSpan.classList.add('message-time');
    const now = new Date();
    timeSpan.textContent = now.toLocaleTimeString();

    headerDiv.appendChild(senderSpan);
    headerDiv.appendChild(timeSpan);

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');

    // Format the message text
    const lines = messageData.message_text.split('\n');
    const formattedLines = lines.map(line => {
        const tabCount = (line.match(/^\t+/) || [''])[0].length;
        const indentClass = `indent-${tabCount}`;
        let trimmedLine = line.replace(/^\t+/, '');
        trimmedLine = trimmedLine.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        return `<span class="${indentClass}">${trimmedLine}</span>`;
    }).join('<br>');

    contentDiv.innerHTML = formattedLines;

    messageDiv.appendChild(headerDiv);
    messageDiv.appendChild(contentDiv);

    // Add tool_calls if they exist
    if (messageData.tool_calls) {
        const toolCallsDiv = document.createElement('div');
        toolCallsDiv.classList.add('tool-calls');

        // Optional: Add a label
        const label = document.createElement('strong');
        label.textContent = 'Tool Calls: ';
        toolCallsDiv.appendChild(label);

        // Handle line breaks in tool_calls
        const toolCallsText = messageData.tool_calls.replace(/\n/g, '<br>');
        const toolCallsContent = document.createElement('span');
        toolCallsContent.innerHTML = toolCallsText;
        toolCallsDiv.appendChild(toolCallsContent);

        messageDiv.appendChild(toolCallsDiv);
    }

    return messageDiv;
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}