// static/location-hub.js

/**
 * Success handler for the 'Describe Place' AJAX form.
 * Inserts or updates the place description section with animation.
 */
function placeDescriptionGenerationSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Success', 'success');

        const container = document.getElementById('place-description-section');
        if (!container) {
            console.error('Place description section not found.');
            return;
        }

        // Reference to the content div
        const contentDiv = container.querySelector('.content');

        // Reference to the place-description div
        const placeDescriptionDiv = container.querySelector('#place-description');

        // Update the description text
        if (placeDescriptionDiv) {
            placeDescriptionDiv.querySelector('p').textContent = data.description || '';

            // Update or remove the voice line URL
            if (data.voice_line_url && data.voice_line_url !== 'None' && data.voice_line_url !== 'null') {
                console.log('Voice line url was correct. Replacing the previous file url with the new one.')
                placeDescriptionDiv.setAttribute('data-file-url', data.voice_line_url);
            } else {
                console.log('Voice line not valid. Removing data-file-url.')
                placeDescriptionDiv.removeAttribute('data-file-url');
            }

            // Add animation class
            placeDescriptionDiv.classList.add('new-place-description');

            // Trigger reflow to restart the animation
            void placeDescriptionDiv.offsetWidth;
            placeDescriptionDiv.classList.remove('new-place-description');
            placeDescriptionDiv.classList.add('new-place-description');

            // Initialize audio playback for the updated element
            initAudioPlayback();
        } else {
            console.log('place-description div didn\'t exist, so I will create it.')
            // If place-description div doesn't exist, create it
            const newPlaceDescriptionDiv = document.createElement('div');
            newPlaceDescriptionDiv.classList.add('place-description', 'new-place-description');
            newPlaceDescriptionDiv.id = 'place-description';

            if (data.voice_line_url && data.voice_line_url !== 'None' && data.voice_line_url !== 'null') {
                console.log('Voice line url was correct. Replacing the previous file url with the new one.')
                newPlaceDescriptionDiv.setAttribute('data-file-url', data.voice_line_url);
            }

            const p = document.createElement('p');
            p.textContent = data.description || '';
            newPlaceDescriptionDiv.appendChild(p);

            const playIcon = document.createElement('i');
            playIcon.classList.add('fas', 'play-icon');
            newPlaceDescriptionDiv.appendChild(playIcon);
            newPlaceDescriptionDiv.appendChild(createWaveformDiv());

            contentDiv.innerHTML = ''; // Clear existing content
            contentDiv.appendChild(newPlaceDescriptionDiv);

            // Add animation
            newPlaceDescriptionDiv.classList.add('new-place-description');

            // Trigger reflow to restart the animation
            void newPlaceDescriptionDiv.offsetWidth;
            newPlaceDescriptionDiv.classList.remove('new-place-description');
            newPlaceDescriptionDiv.classList.add('new-place-description');

            // Initialize audio playback
            initAudioPlayback();
        }

        // Ensure the collapsible section is visible by toggling classes
        container.classList.remove('hidden-section');
        container.classList.add('visible-section');

        // Ensure the collapsible section is open
        container.querySelector('.collapsible').classList.add('active');
        contentDiv.style.display = 'block';

    } else {
        showToast(data.error || 'An error occurred', 'error');
    }
}

function animateWeatherIcon() {
    const weatherIcon = document.querySelector('.weather-icon i');
    if (weatherIcon && weatherIcon.classList.contains('fa-sun')) {
        weatherIcon.classList.add('sun-rotate');
    }
}

function pageInit(){
    animateWeatherIcon();
}
