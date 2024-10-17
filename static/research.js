// static/research.js

function resolveResearchSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Research resolved successfully.', 'success');

        // Hide the 'Enter Research Goal' collapsible section.
        const researchGoalSection = document.querySelector('.collapsible-section');
        if (researchGoalSection) {
            researchGoalSection.style.display = 'none';
        }

        // Create the 'Research Resolution Result' collapsible section.
        const researchContainer = document.querySelector('.research-container');

        if (researchContainer) {
            // Create the collapsible section
            const collapsibleSection = document.createElement('div');
            collapsibleSection.classList.add('collapsible-section');

            // Create the collapsible button
            const collapsibleButton = document.createElement('button');
            collapsibleButton.classList.add('collapsible');
            const icon = document.createElement('i');
            icon.classList.add('fas', 'fa-check');
            collapsibleButton.appendChild(icon);
            collapsibleButton.appendChild(document.createTextNode(' Research Resolution Result'));

            // Create the content div
            const contentDiv = document.createElement('div');
            contentDiv.classList.add('content');

            // Create the 'research-result' div
            const researchResultDiv = document.createElement('div');
            researchResultDiv.classList.add('research-result');

            // Create the 'narration' div
            const narrationDiv = document.createElement('div');
            narrationDiv.classList.add('narration');
            narrationDiv.setAttribute('data-file-url', data.result.narrative_voice_line_url || '');

            const narrationH3 = document.createElement('h3');
            narrationH3.textContent = 'Narration';
            const narrationP = document.createElement('p');
            narrationP.textContent = data.result.narrative;
            const narrationIcon = document.createElement('i');
            narrationIcon.classList.add('fas', 'play-icon');

            narrationDiv.appendChild(narrationH3);
            narrationDiv.appendChild(narrationP);
            narrationDiv.appendChild(narrationIcon);

            // Similarly for 'outcome' div
            const outcomeDiv = document.createElement('div');
            outcomeDiv.classList.add('outcome');
            outcomeDiv.setAttribute('data-file-url', data.result.outcome_voice_line_url || '');

            const outcomeH3 = document.createElement('h3');
            outcomeH3.textContent = 'Outcome';
            const outcomeP = document.createElement('p');
            outcomeP.textContent = data.result.outcome;
            const outcomeIcon = document.createElement('i');
            outcomeIcon.classList.add('fas', 'play-icon');

            outcomeDiv.appendChild(outcomeH3);
            outcomeDiv.appendChild(outcomeP);
            outcomeDiv.appendChild(outcomeIcon);

            // Append 'narration' and 'outcome' divs to 'research-result' div
            researchResultDiv.appendChild(narrationDiv);
            researchResultDiv.appendChild(outcomeDiv);

            // Append 'research-result' div to 'content' div
            contentDiv.appendChild(researchResultDiv);

            // Append collapsible button and content div to collapsible section
            collapsibleSection.appendChild(collapsibleButton);
            collapsibleSection.appendChild(contentDiv);

            // Append the new collapsible section to the 'research-container'
            researchContainer.appendChild(collapsibleSection);

            // Initialize the collapsible behavior
            collapsibleButton.addEventListener('click', function() {
                this.classList.toggle('active');
                if (contentDiv.style.display === 'block') {
                    contentDiv.style.display = 'none';
                } else {
                    contentDiv.style.display = 'block';
                }
            });

            // Initialize audio playback for the new elements
            initAudioPlayback();

            // Optionally, simulate a click to open the collapsible
            collapsibleButton.click();

            // Now, create the 'Modify Characters' section
            if (data.characters && data.characters.length > 0) {
                const modifyCharactersSection = document.createElement('div');
                modifyCharactersSection.classList.add('collapsible-section');

                const modifyCollapsibleButton = document.createElement('button');
                modifyCollapsibleButton.classList.add('collapsible');
                const modifyIcon = document.createElement('i');
                modifyIcon.classList.add('fas', 'fa-user-edit');
                modifyCollapsibleButton.appendChild(modifyIcon);
                modifyCollapsibleButton.appendChild(document.createTextNode(' Modify Characters'));

                const modifyContentDiv = document.createElement('div');
                modifyContentDiv.classList.add('content');

                const form = document.createElement('form');
                form.action = data.form_action || '';
                form.method = 'post';
                form.classList.add('ajax-form');
                form.dataset.successHandler = 'modifyCharactersSuccess';

                const inputFormType = document.createElement('input');
                inputFormType.type = 'hidden';
                inputFormType.name = 'form_type';
                inputFormType.value = 'modify_characters';
                form.appendChild(inputFormType);

                data.characters.forEach(function(character) {
                    const characterDiv = document.createElement('div');
                    characterDiv.classList.add('character-modification');

                    const h3 = document.createElement('h3');
                    h3.textContent = character.name;

                    const labelDescription = document.createElement('label');
                    labelDescription.setAttribute('for', 'description_' + character.identifier);
                    labelDescription.textContent = 'Description:';
                    const textareaDescription = document.createElement('textarea');
                    textareaDescription.id = 'description_' + character.identifier;
                    textareaDescription.name = 'description_' + character.identifier;
                    textareaDescription.textContent = character.description;

                    const labelEquipment = document.createElement('label');
                    labelEquipment.setAttribute('for', 'equipment_' + character.identifier);
                    labelEquipment.textContent = 'Equipment:';
                    const textareaEquipment = document.createElement('textarea');
                    textareaEquipment.id = 'equipment_' + character.identifier;
                    textareaEquipment.name = 'equipment_' + character.identifier;
                    textareaEquipment.textContent = character.equipment;

                    const labelHealth = document.createElement('label');
                    labelHealth.setAttribute('for', 'health_' + character.identifier);
                    labelHealth.textContent = 'Health:';
                    const textareaHealth = document.createElement('textarea');
                    textareaHealth.id = 'health_' + character.identifier;
                    textareaHealth.name = 'health_' + character.identifier;
                    textareaHealth.textContent = character.health;

                    characterDiv.appendChild(h3);
                    characterDiv.appendChild(labelDescription);
                    characterDiv.appendChild(textareaDescription);
                    characterDiv.appendChild(labelEquipment);
                    characterDiv.appendChild(textareaEquipment);
                    characterDiv.appendChild(labelHealth);
                    characterDiv.appendChild(textareaHealth);

                    form.appendChild(characterDiv);
                });

                const submitButton = document.createElement('button');
                submitButton.type = 'submit';
                submitButton.classList.add('action-button');
                const saveIcon = document.createElement('i');
                saveIcon.classList.add('fas', 'fa-save');
                submitButton.appendChild(saveIcon);
                submitButton.appendChild(document.createTextNode(' Save Changes'));

                form.appendChild(submitButton);

                modifyContentDiv.appendChild(form);

                modifyCharactersSection.appendChild(modifyCollapsibleButton);
                modifyCharactersSection.appendChild(modifyContentDiv);

                researchContainer.appendChild(modifyCharactersSection);

                modifyCollapsibleButton.addEventListener('click', function() {
                    this.classList.toggle('active');
                    if (modifyContentDiv.style.display === 'block') {
                        modifyContentDiv.style.display = 'none';
                    } else {
                        modifyContentDiv.style.display = 'block';
                    }
                });

                handleAjaxFormSubmit(form, {
                    onSuccess: window['modifyCharactersSuccess'],
                });
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