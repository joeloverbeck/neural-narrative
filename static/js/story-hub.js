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
                itemsList = document.createElement('div');
                itemsList.classList.add(options.listClass);
                contentDiv = context.form.closest('.content');
                const noItemsMessage = contentDiv.querySelector('p');
                if (noItemsMessage) {
                    noItemsMessage.remove();
                }
                contentDiv.appendChild(itemsList);
            } else {
                contentDiv = itemsList.parentElement;
            }

            data[options.itemsKey].forEach((item, i) => {
                const itemIndex = startIndex + i;
                const itemElement = options.createItemElement(item, itemIndex);
                itemsList.appendChild(itemElement);

                if (typeof options.afterItemAdded === 'function') {
                    options.afterItemAdded(item, itemIndex, context, options);
                }
            });

            if (typeof options.initItemClickEvents === 'function') {
                options.initItemClickEvents(options.itemClass, options.actionName);
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

function openModal(index, actionName) {
    document.getElementById(`modal-${actionName}-${index}`).style.display = 'block';
}

function closeModal(index, actionName) {
    document.getElementById(`modal-${actionName}-${index}`).style.display = 'none';
}

function createModal(itemContent, index, itemType, actionName) {
    const modal = document.createElement('div');
    modal.id = `modal-${actionName}-${index}`;
    modal.classList.add('modal');

    const modalContent = document.createElement('div');
    modalContent.classList.add('modal-content');

    const closeSpan = document.createElement('span');
    closeSpan.classList.add('close');
    closeSpan.innerHTML = '&times;';
    closeSpan.onclick = function() {
        closeModal(index, actionName);
    };

    const h2 = document.createElement('h2');
    h2.textContent = `${itemType} ${index + 1}`;

    const p = document.createElement('p');
    p.textContent = itemContent;

    const form = document.createElement('form');
    form.action = window.location.href;
    form.method = 'post';

    const inputIndex = document.createElement('input');
    inputIndex.type = 'hidden';
    inputIndex.name = 'item_index';
    inputIndex.value = index;

    const inputAction = document.createElement('input');
    inputAction.type = 'hidden';
    inputAction.name = 'submit_action';
    inputAction.value = `delete_${actionName}`;

    const button = document.createElement('button');
    button.type = 'submit';
    button.classList.add('delete-button');

    const icon = document.createElement('i');
    icon.classList.add('fas', 'fa-trash-alt');
    button.appendChild(icon);
    button.appendChild(document.createTextNode(' Delete'));

    form.appendChild(inputIndex);
    form.appendChild(inputAction);
    form.appendChild(button);

    modalContent.appendChild(closeSpan);
    modalContent.appendChild(h2);
    modalContent.appendChild(p);
    modalContent.appendChild(form);

    modal.appendChild(modalContent);

    return modal;
}

function createItemElement(itemContent, index, itemType, itemClass, actionName) {
    const itemElement = document.createElement('div');
    itemElement.classList.add(itemClass);
    itemElement.setAttribute('data-index', index);

    itemElement.onclick = function() {
        openModal(index, actionName);
    };

    const header = document.createElement('h3');
    header.textContent = `${itemType} ${index + 1}`;

    const paragraph = document.createElement('p');
    const truncatedItem = itemContent.length > 150 ? `${itemContent.substring(0, 150)}...` : itemContent;
    paragraph.textContent = truncatedItem;

    itemElement.appendChild(header);
    itemElement.appendChild(paragraph);

    return itemElement;
}

function generateAntagonistsSuccess(data, context) {
    generateItemsSuccess(data, context, {
        defaultSuccessMessage: 'Antagonists generated successfully.',
        itemsKey: 'antagonists',
        listSelector: '.antagonists-list',
        listClass: 'antagonists-list',
        itemSelector: '.antagonists-list .antagonist-item',
        itemClass: 'antagonist-item',
        actionName: 'antagonist',
        createItemElement: function(item, index) {
            return createItemElement(item, index, 'Antagonist', 'antagonist-item', 'antagonist');
        },
        initItemClickEvents: initItemClickEvents,
        afterItemAdded: function(item, itemIndex, context, options) {
            const contentDiv = context.form.closest('.content');
            const modal = createModal(item, itemIndex, 'Antagonist', 'antagonist');
            contentDiv.appendChild(modal);
        }
    });
}

function generatePlotBlueprintsSuccess(data, context) {
    generateItemsSuccess(data, context, {
        defaultSuccessMessage: 'Plot blueprints generated successfully.',
        itemsKey: 'plot_blueprints',
        listSelector: '.plot-blueprints-list',
        listClass: 'plot-blueprints-list',
        itemSelector: '.plot-blueprints-list .plot-blueprint-item',
        itemClass: 'plot-blueprint',
        actionName: 'plot_blueprint',
        createItemElement: function(item, index) {
            return createItemElement(item, index, 'Plot Blueprint', 'plot-blueprint-item', 'plot_blueprint');
        },
        initItemClickEvents: initItemClickEvents,
        afterItemAdded: function(item, itemIndex, context, options) {
            // Create and append the modal
            const contentDiv = context.form.closest('.content');
            const modal = createModal(item, itemIndex, 'Plot Blueprint', 'plot_blueprint');
            contentDiv.appendChild(modal);
        }
    });
}

function generateScenariosSuccess(data, context) {
    generateItemsSuccess(data, context, {
        defaultSuccessMessage: 'Scenarios generated successfully.',
        itemsKey: 'scenarios',
        listSelector: '.scenarios-list',
        listClass: 'scenarios-list',
        itemSelector: '.scenarios-list .item-form',
        createItemElement: createItemForm.bind(null, 'delete_scenario'),
        initItemForms: initItemForms
    });
}

function generateDilemmasSuccess(data, context) {
    generateItemsSuccess(data, context, {
        defaultSuccessMessage: 'Dilemmas generated successfully.',
        itemsKey: 'dilemmas',
        listSelector: '.dilemmas-list',
        listClass: 'dilemmas-list',
        itemSelector: '.dilemmas-list .item-form',
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

function generatePlotTwistsSuccess(data, context) {
    generateItemsSuccess(data, context, {
        defaultSuccessMessage: 'Plot twists generated successfully.',
        itemsKey: 'plot_twists',
        listSelector: '.plot-twists-list',
        listClass: 'plot-twists-list',
        itemSelector: '.plot-twists-list .item-form',
        createItemElement: createItemForm.bind(null, 'delete_plot_twist'),
        initItemForms: initItemForms
    });
}

function generateLoreAndLegendsSuccess(data, context) {
    generateItemsSuccess(data, context, {
        defaultSuccessMessage: 'Lore and legends generated successfully.',
        itemsKey: 'lore_and_legends',
        listSelector: '.lore-and-legends-list',
        listClass: 'lore-and-legends-list',
        itemSelector: '.lore-and-legends-list .lore-or-legend-item',
        itemClass: 'lore-or-legend',
        actionName: 'lore_or_legend',
        createItemElement: function(item, index) {
            return createItemElement(item, index, 'Lore or Legend', 'lore-or-legend-item', 'lore_or_legend');
        },
        initItemClickEvents: initItemClickEvents,
        afterItemAdded: function(item, itemIndex, context, options) {
            // Create and append the modal
            const contentDiv = context.form.closest('.content');
            const modal = createModal(item, itemIndex, 'Lore or Legend', 'lore_or_legend');
            contentDiv.appendChild(modal);
        }
    });
}

function initItemClickEvents(itemClass, actionName) {
    const items = document.querySelectorAll(`.${itemClass}`);

    items.forEach(function(item) {
        item.onclick = function() {
            const index = parseInt(this.getAttribute('data-index'));
            openModal(index, actionName);
        };
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

function initPlotBlueprintItemForms() {
    const plotBlueprintItems = document.querySelectorAll('.plot-blueprint-item');

    plotBlueprintItems.forEach(function(item) {
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
    // Initialize event listeners for plot blueprints
    initItemClickEvents('plot-blueprint-item', 'plot_blueprint');

    // Initialize event listeners for antagonists
    initItemClickEvents('antagonist-item', 'antagonist');

    // Initialize event listeners for other item forms if needed
    initItemForms();
}