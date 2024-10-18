// static/research.js

function resolveActionSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Research resolved successfully.', 'success');

        // Hide the 'Enter Research Goal' collapsible section.
        const researchGoalSection = document.querySelector('.collapsible-section');
        if (researchGoalSection) {
            researchGoalSection.style.display = 'none';
        }

        // Create the 'Research Resolution Result' collapsible section.
        const researchContainer = document.querySelector('#action-result-container');

        if (researchContainer) {
            const researchResultDiv = createActionResultDiv(data.result);
            const researchCollapsibleSection = createCollapsibleSection(
                'Research Resolution Result',
                'fa-check',
                researchResultDiv,
                true
            );
            researchContainer.appendChild(researchCollapsibleSection);

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
                researchContainer.appendChild(modifyCharactersSection);
            }
        }
    } else {
        showToast(data.error || 'An error occurred while resolving research.', 'error');
    }
}

function modifyCharactersSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Character changes saved successfully.', 'success');
    } else {
        showToast(data.error || 'An error occurred while saving character changes.', 'error');
    }
}