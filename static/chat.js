// static/chat.js

document.addEventListener('DOMContentLoaded', function () {
    // Function to scroll the chat window to the bottom
    function scrollToBottom() {
        const chatWindow = document.getElementById('chat-window');
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Call scrollToBottom after the page loads
    scrollToBottom();

    // Function to handle click events on chat bubbles
    function handleChatBubbleClick(event) {
        var fileUrl = event.currentTarget.getAttribute('data-file-url');
        playAudio(fileUrl);
    }

    // Attach event listeners to chat bubbles and ambient messages
    var chatBubbles = document.querySelectorAll('.chat-bubble, .ambient-message');
    chatBubbles.forEach(function(chatBubble) {
        chatBubble.addEventListener('click', handleChatBubbleClick);
        chatBubble.style.cursor = 'pointer';
    });

    // Call scrollToBottom whenever a new message is added to the chat
    const chatForm = document.querySelector('.chat-form');
    chatForm.addEventListener('submit', function() {
        setTimeout(scrollToBottom, 100); // Delay to wait for the message to be added
    });
});

// Existing code for message text formatting
document.addEventListener('DOMContentLoaded', function () {
    var messageTexts = document.querySelectorAll('.message-text');

    messageTexts.forEach(function (messageText) {
        var content = messageText.innerHTML;

        var updatedContent = content.replace(/^\*(.*?)\*\s*(.*)/, '<span class="narration">$1</span><div class="narration-break"></div>$2');

        updatedContent = updatedContent.replace(/\*(.*?)\*/g, '<span class="narration">$1</span>');

        messageText.innerHTML = updatedContent;
    });
});