// static/audio-playback.js

let currentAudio = null; // Global variable to keep track of the current playing audio

function playAudio(fileUrl, element) {
    if (!fileUrl || fileUrl === 'None' || fileUrl === 'null') {
        alert('The audio file is not available.');
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
            alert('The audio file could not be loaded.');
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
            alert('The audio file couldn\'t be played.');
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

document.addEventListener('DOMContentLoaded', function () {
    // Initialize audio playback elements on page load
    initAudioPlayback();
});