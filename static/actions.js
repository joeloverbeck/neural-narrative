// static/actions.js

function createNarrationOutcomeDiv(sectionTitle, textContent, voiceLineUrl) {
    const sectionDiv = document.createElement('div');
    sectionDiv.classList.add(sectionTitle.toLowerCase());
    sectionDiv.setAttribute('data-file-url', voiceLineUrl || '');

    const h3 = document.createElement('h3');
    h3.textContent = sectionTitle;

    const p = document.createElement('p');
    p.textContent = textContent;

    const playIcon = document.createElement('i');
    playIcon.classList.add('fas', 'fa-play', 'play-icon');

    const waveformDiv = createWaveformDiv();

    sectionDiv.append(h3, p, playIcon, waveformDiv);

    return sectionDiv;
}

function createActionResultDiv(dataResult) {
    const actionResultDiv = document.createElement('div');
    actionResultDiv.classList.add('action-result');

    const narrationDiv = createNarrationOutcomeDiv(
        'Narration',
        dataResult.narrative,
        dataResult.narrative_voice_line_url
    );
    const outcomeDiv = createNarrationOutcomeDiv(
        'Outcome',
        dataResult.outcome,
        dataResult.outcome_voice_line_url
    );

    actionResultDiv.append(narrationDiv, outcomeDiv);

    return actionResultDiv;
}

function createCharacterModificationForm(characters, formAction) {
    const form = document.createElement('form');
    form.action = formAction || '';
    form.method = 'post';
    form.classList.add('ajax-form');
    form.dataset.successHandler = 'modifyCharactersSuccess';

    const inputFormType = document.createElement('input');
    inputFormType.type = 'hidden';
    inputFormType.name = 'form_type';
    inputFormType.value = 'modify_characters';
    form.appendChild(inputFormType);

    characters.forEach((character) => {
        const characterDiv = document.createElement('div');
        characterDiv.classList.add('character-modification');

        const h3 = document.createElement('h3');
        h3.textContent = character.name;

        const fields = [
            { label: 'Description:', key: 'description', value: character.description },
            { label: 'Equipment:', key: 'equipment', value: character.equipment },
            { label: 'Health:', key: 'health', value: character.health },
        ];

        characterDiv.appendChild(h3);

        fields.forEach((field) => {
            const id = `${field.key}_${character.identifier}`;
            const label = document.createElement('label');
            label.setAttribute('for', id);
            label.textContent = field.label;

            const textarea = document.createElement('textarea');
            textarea.id = id;
            textarea.name = id;
            textarea.textContent = field.value;

            characterDiv.append(label, textarea);
        });

        form.appendChild(characterDiv);
    });

    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.classList.add('action-button');

    const saveIcon = document.createElement('i');
    saveIcon.classList.add('fas', 'fa-save');
    submitButton.append(saveIcon, document.createTextNode(' Save Changes'));

    form.appendChild(submitButton);

    // Initialize the AJAX form submission
    handleAjaxFormSubmit(form, {
        onSuccess: window['modifyCharactersSuccess'],
    });

    return form;
}

function resolveActionSuccess(data, context) {
    if (data.success) {
        const actionName = data.action_name || 'Action';
        showToast(data.message || `${actionName} resolved successfully.`, 'success');

        // Hide the 'Enter {Action} Goal' collapsible section.
        const actionGoalSection = document.querySelector('.collapsible-section');
        if (actionGoalSection) {
            actionGoalSection.style.display = 'none';
        }

        // Create the '{Action} Resolution Result' collapsible section.
        const actionContainer = document.querySelector('#action-result-container');

        if (actionContainer) {
            const actionResultDiv = createActionResultDiv(data.result);
            const actionCollapsibleSection = createCollapsibleSection(
                `${actionName} Resolution Result`,
                'fa-check',
                actionResultDiv,
                true
            );
            actionContainer.appendChild(actionCollapsibleSection);

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
                actionContainer.appendChild(modifyCharactersSection);
            }
        }
    } else {
        showToast(data.error || 'An error occurred while resolving action.', 'error');
    }
}

function modifyCharactersSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Character changes saved successfully.', 'success');
    } else {
        showToast(data.error || 'An error occurred while saving character changes.', 'error');
    }
}