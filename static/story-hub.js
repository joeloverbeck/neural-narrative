// static/story-hub.js

function generateItemsSuccess(data, context, options) {
    if (data.success) {
        showToast(data.message || options.defaultSuccessMessage, 'success');

        if (data[options.itemsKey]) {
            const existingItems = document.querySelectorAll(options.itemSelector);
            const startIndex = existingItems.length;

            let itemsList = document.querySelector(options.listSelector);
            let contentDiv = null;

            if (!itemsList) {
                // Create items-list div and append to contentDiv
                itemsList = document.createElement('div');
                itemsList.classList.add(options.listClass);
                // Find the content div
                contentDiv = context.form.closest('.content');
                // Remove the "No items generated yet." message if it exists
                const noItemsMessage = contentDiv.querySelector('p');
                if (noItemsMessage) {
                    noItemsMessage.remove();
                }
                contentDiv.appendChild(itemsList);
            } else {
                // If itemsList exists, get its parent as contentDiv
                contentDiv = itemsList.parentElement;
            }

            // Append each new item to the items list
            data[options.itemsKey].forEach((item, i) => {
                const itemIndex = startIndex + i;
                const itemElement = options.createItemElement(item, itemIndex);
                itemsList.appendChild(itemElement);
            });

            // Re-initialize event listeners for new forms
            if (typeof options.initItemForms === 'function') {
                options.initItemForms();
            }
        }
    } else {
        showToast(data.error || 'An error occurred', 'error');
    }
}

function createItemForm(submitAction, item, index) {
    // Create the form
    const form = document.createElement('form');
    form.action = window.location.href; // Use current URL
    form.method = 'post';
    form.classList.add('item-form');

    // Create hidden input for submit_action
    const inputAction = document.createElement('input');
    inputAction.type = 'hidden';
    inputAction.name = 'submit_action';
    inputAction.value = submitAction;

    // Create hidden input for item_index
    const inputIndex = document.createElement('input');
    inputIndex.type = 'hidden';
    inputIndex.name = 'item_index';
    inputIndex.value = index;

    // Create the button
    const button = document.createElement('button');
    button.type = 'submit';
    button.classList.add('post-it');

    // Create the icon
    const icon = document.createElement('i');
    icon.classList.add('fas', 'fa-thumbtack');

    // Create the paragraph
    const p = document.createElement('p');
    p.textContent = item;

    // Append icon and paragraph to button
    button.appendChild(icon);
    button.appendChild(p);

    // Append inputs and button to form
    form.appendChild(inputAction);
    form.appendChild(inputIndex);
    form.appendChild(button);

    return form;
}

function openModal(index) {
    document.getElementById('modal-' + index).style.display = 'block';
}

function closeModal(index) {
    document.getElementById('modal-' + index).style.display = 'none';
}

function createModal(concept, index) {
    // Create the modal div
    const modal = document.createElement('div');
    modal.id = `modal-${index}`;
    modal.classList.add('modal');

    // Create modal-content div
    const modalContent = document.createElement('div');
    modalContent.classList.add('modal-content');

    // Create the close span
    const closeSpan = document.createElement('span');
    closeSpan.classList.add('close');
    closeSpan.innerHTML = '&times;';
    closeSpan.onclick = function() {
        closeModal(index);
    };

    // Create h2 element for Concept title
    const h2 = document.createElement('h2');
    h2.textContent = `Concept ${index + 1}`;

    // Create p element for concept text
    const p = document.createElement('p');
    p.textContent = concept;

    // Create form for deleting concept
    const form = document.createElement('form');
    form.action = window.location.href; // Use current URL
    form.method = 'post';

    // Create hidden input for item_index
    const inputIndex = document.createElement('input');
    inputIndex.type = 'hidden';
    inputIndex.name = 'item_index';
    inputIndex.value = index;

    // Create hidden input for submit_action
    const inputAction = document.createElement('input');
    inputAction.type = 'hidden';
    inputAction.name = 'submit_action';
    inputAction.value = 'delete_concept';

    // Create delete button
    const button = document.createElement('button');
    button.type = 'submit';
    button.classList.add('delete-button');

    const icon = document.createElement('i');
    icon.classList.add('fas', 'fa-trash-alt');
    button.appendChild(icon);
    button.appendChild(document.createTextNode(' Delete'));

    // Append inputs and button to form
    form.appendChild(inputIndex);
    form.appendChild(inputAction);
    form.appendChild(button);

    // Append elements to modal-content
    modalContent.appendChild(closeSpan);
    modalContent.appendChild(h2);
    modalContent.appendChild(p);
    modalContent.appendChild(form);

    // Append modal-content to modal
    modal.appendChild(modalContent);

    return modal;
}

function createConceptItem(concept, index) {
    // Create a concept-item div
    const conceptItem = document.createElement('div');
    conceptItem.classList.add('concept-item');
    conceptItem.setAttribute('data-index', index);

    // Set the onclick attribute to call openModal with the current index
    conceptItem.onclick = function() {
        openModal(index);
    };

    // Create the h3 element for the concept title
    const header = document.createElement('h3');
    header.textContent = `Concept ${index + 1}`; // Assuming index starts at 0

    // Create the p element for the concept description
    const paragraph = document.createElement('p');

    // Truncate the concept text to 150 characters and add ellipsis if necessary
    const truncatedConcept = concept.length > 150 ? `${concept.substring(0, 150)}...` : concept;
    paragraph.textContent = truncatedConcept;

    // Append the header and paragraph to the concept-item div
    conceptItem.appendChild(header);
    conceptItem.appendChild(paragraph);

    return conceptItem;
}

function generateConceptsSuccess(data, context) {
    generateItemsSuccess(data, context, {
        defaultSuccessMessage: 'Concepts generated successfully.',
        itemsKey: 'concepts',
        listSelector: '.concepts-list',
        listClass: 'concepts-list',
        itemSelector: '.concepts-list .concept-item',
        createItemElement: createConceptItem,
        initItemForms: initConceptItemForms
    });
}

function generateInterestingSituationsSuccess(data, context) {
    generateItemsSuccess(data, context, {
        defaultSuccessMessage: 'Interesting situations generated successfully.',
        itemsKey: 'interesting_situations',
        listSelector: '.interesting-situations-list',
        listClass: 'interesting-situations-list',
        itemSelector: '.interesting-situations-list .item-form',
        createItemElement: createItemForm.bind(null, 'delete_situation'),
        initItemForms: initItemForms
    });
}

function generateInterestingDilemmasSuccess(data, context) {
    generateItemsSuccess(data, context, {
        defaultSuccessMessage: 'Interesting dilemmas generated successfully.',
        itemsKey: 'interesting_dilemmas',
        listSelector: '.interesting-dilemmas-list',
        listClass: 'interesting-dilemmas-list',
        itemSelector: '.interesting-dilemmas-list .item-form',
        createItemElement: createItemForm.bind(null, 'delete_dilemma'),
        initItemForms: initItemForms
    });
}

function generateGoalsSuccess(data, context) {
    generateItemsSuccess(data, context, {
        defaultSuccessMessage: 'Goals generated successfully.',
        itemsKey: 'goals',
        listSelector: '.goals-list',
        listClass: 'goals-list',
        itemSelector: '.goals-list .item-form',
        createItemElement: createItemForm.bind(null, 'delete_goal'),
        initItemForms: initItemForms
    });
}

// Close modal when clicking outside of content
window.onclick = function(event) {
    let modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
}

function initConceptItemForms() {
    const conceptItems = document.querySelectorAll('.concept-item');

    conceptItems.forEach(function(item) {
        item.onclick = function() {
            const index = parseInt(this.getAttribute('data-index'));
            openModal(index);
        };
    });
}

function initItemForms() {
    const itemForms = document.querySelectorAll('.item-form');

    itemForms.forEach(function(form) {
        // Avoid adding multiple event listeners to the same form
        if (!form.classList.contains('event-attached')) {
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                const itemButton = form.querySelector('.post-it');
                itemButton.classList.add('fade-out');
                setTimeout(function() {
                    form.submit();
                }, 500);
            });
            form.classList.add('event-attached');
        }
    });
}

function pageInit() {
    // Initialize event listeners for concept items
    initConceptItemForms();

    // Initialize event listeners for item forms
    initItemForms();
}