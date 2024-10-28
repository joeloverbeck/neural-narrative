// static/travel.js

// JavaScript function to handle the success response from travel action
function travelSuccess(data, context) {
    if (data.success) {
        showToast('Travel narration generated.', 'success');

        // Hide or remove the travel form
        const travelForm = document.getElementById('travel-form');
        if (travelForm) {
            travelForm.remove(); // Or use travelForm.style.display = 'none';
        }

        const container = document.getElementById('travel-narration-container');
        if (container) {
            // Clear previous content
            container.innerHTML = '';

            // Create narration and outcome elements
            const narrationDiv = createNarrationOutcomeDiv('Narration', data.narrative, data.narrative_voice_line_url);
            const outcomeDiv = createNarrationOutcomeDiv('Outcome', data.outcome, data.outcome_voice_line_url);

            container.appendChild(narrationDiv);
            container.appendChild(outcomeDiv);

            // Create 'Enter Destination Area' button
            const form = document.createElement('form');
            form.action = data.enter_area_url; // Use URL from data
            form.method = 'post';

            const inputAction = document.createElement('input');
            inputAction.type = 'hidden';
            inputAction.name = 'submit_action';
            inputAction.value = 'enter_area';
            form.appendChild(inputAction);

            const inputDestination = document.createElement('input');
            inputDestination.type = 'hidden';
            inputDestination.name = 'destination_identifier';
            inputDestination.value = data.destination_identifier;
            form.appendChild(inputDestination);

            const button = document.createElement('button');
            button.type = 'submit';
            button.classList.add('action-button');

            const icon = document.createElement('i');
            icon.classList.add('fas', 'fa-door-open');
            button.appendChild(icon);
            button.appendChild(document.createTextNode(' Enter ' + data.destination_name));

            form.appendChild(button);

            container.appendChild(form);
        }

        // Initialize audio playback for the new elements
        initAudioPlayback();
    } else {
        showToast(data.error || 'Failed to generate travel narration.', 'error');
    }
}