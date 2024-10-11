// static/audio-playback.js

document.addEventListener('DOMContentLoaded', function () {
    // Function to initialize audio playback elements
    function initAudioPlayback() {
        var audioElements = document.querySelectorAll('[data-file-url]');
        audioElements.forEach(function(element) {
            element.addEventListener('click', function(event) {
                var fileUrl = event.currentTarget.getAttribute('data-file-url');
                playAudio(fileUrl, event.currentTarget);
            });
            element.style.cursor = 'pointer';
        });
    }

    // Initialize audio playback elements on page load
    initAudioPlayback();
});

function playAudio(fileUrl, element) {
    if (fileUrl && fileUrl !== 'None' && fileUrl !== 'null') {
        var audio = new Audio(fileUrl);

        // Add 'playing' class when audio starts
        audio.addEventListener('playing', function() {
            if (element) {
                element.classList.add('playing');
            }
        });

        // Remove 'playing' class when audio ends
        audio.addEventListener('ended', function() {
            if (element) {
                element.classList.remove('playing');
            }
        });

        // Also handle pause event (in case audio is paused manually)
        audio.addEventListener('pause', function() {
            if (element) {
                element.classList.remove('playing');
            }
        });

        audio.onerror = function() {
            console.error('Error occurred while loading audio:', audio.error);
            alert('The audio file could not be loaded.');
        };

        audio.play().catch(function(error) {
            console.error('Error occurred while playing audio:', error);
            alert('The audio file couldn\'t be played.');
        });
    } else {
        alert('The audio file is not available.');
    }
}