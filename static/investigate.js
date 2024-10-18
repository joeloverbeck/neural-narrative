// static/investigate.js

function resolveActionSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Investigate resolved successfully.', 'success');

        // Hide the 'Enter Investigate Goal' collapsible section.
        const investigateGoalSection = document.querySelector('.collapsible-section');
        if (investigateGoalSection) {
            investigateGoalSection.style.display = 'none';
        }

        // Create the 'Investigate Resolution Result' collapsible section.
        const investigateContainer = document.querySelector('#action-result-container');

        if (investigateContainer) {
            const investigateResultDiv = createActionResultDiv(data.result);
            const investigateCollapsibleSection = createCollapsibleSection(
                'Investigate Resolution Result',
                'fa-check',
                investigateResultDiv,
                true
            );
            investigateContainer.appendChild(investigateCollapsibleSection);

            // Initialize audio playback for the new elements
            initAudioPlayback();

            // Create the 'Modify Characters' section if characters are available
            if (data.characters && data.characters.length > 0) {
                const form = createCharacterModificationForm(data.characters, data.form_action);
                const modifyCharactersSection = createCollapsibleSection(
                    'Modify Characters',
                    'fa-user-edit',
                    form
                );
                investigateContainer.appendChild(modifyCharactersSection);
            }
        }
    } else {
        showToast(data.error || 'An error occurred while resolving investigate action.', 'error');
    }
}

function modifyCharactersSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Character changes saved successfully.', 'success');
    } else {
        showToast(data.error || 'An error occurred while saving character changes.', 'error');
    }
}