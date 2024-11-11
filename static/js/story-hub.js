// static/story-hub.js

// Configuration object for different item types
const itemTypeConfigs = {
    antagonist: {
        itemTypeName: 'Antagonist',
        itemsKey: 'antagonists',
        itemClass: 'antagonist-item',
        listClass: 'antagonists-list',
        actionName: 'antagonist',
        iconClass: 'fa-solid fa-skull',
        defaultSuccessMessage: 'Antagonists generated successfully.',
        displayMode: 'modal',
    },
    plot_blueprint: {
        itemTypeName: 'Plot Blueprint',
        itemsKey: 'plot_blueprints',
        itemClass: 'plot-blueprint-item',
        listClass: 'plot-blueprints-list',
        actionName: 'plot_blueprint',
        iconClass: 'fas fa-lightbulb',
        defaultSuccessMessage: 'Plot blueprints generated successfully.',
        displayMode: 'modal',
    },
    scenario: {
        itemTypeName: 'Scenario',
        itemsKey: 'scenarios',
        listClass: 'scenarios-list',
        itemClass: 'item-form',
        actionName: 'scenario',
        defaultSuccessMessage: 'Scenarios generated successfully.',
        displayMode: 'form',
    },
    artifact: {
        itemTypeName: 'Artifact',
        itemsKey: 'artifacts',
        itemClass: 'artifact-item',
        listClass: 'artifacts-list',
        actionName: 'artifact',
        iconClass: 'fas fa-gem',
        defaultSuccessMessage: 'Artifacts generated successfully.',
        displayMode: 'modal',
    },
    dilemma: {
        itemTypeName: 'Dilemma',
        itemsKey: 'dilemmas',
        listClass: 'dilemmas-list',
        itemClass: 'item-form',
        actionName: 'dilemma',
        defaultSuccessMessage: 'Dilemmas generated successfully.',
        displayMode: 'form',
    },
    goal: {
        itemTypeName: 'Goal',
        itemsKey: 'goals',
        listClass: 'goals-list',
        itemClass: 'item-form',
        actionName: 'goal',
        defaultSuccessMessage: 'Goals generated successfully.',
        displayMode: 'form',
    },
    lore_or_legend: {
        itemTypeName: 'Lore or Legend',
        itemsKey: 'lore_and_legends',
        itemClass: 'lore-or-legend-item',
        listClass: 'lore-and-legends-list',
        actionName: 'lore_or_legend',
        iconClass: 'fas fa-dragon',
        defaultSuccessMessage: 'Lore and legends generated successfully.',
        displayMode: 'modal',
    },
    plot_twist: {
        itemTypeName: 'Plot Twist',
        itemsKey: 'plot_twists',
        listClass: 'plot-twists-list',
        itemClass: 'item-form',
        actionName: 'plot_twist',
        defaultSuccessMessage: 'Plot twists generated successfully.',
        displayMode: 'form',
    },
    mystery: {
        itemTypeName: 'Mystery',
        itemsKey: 'mysteries',
        itemClass: 'mystery-item',
        listClass: 'mysteries-list',
        actionName: 'mystery',
        iconClass: 'fas fa-puzzle-piece',
        defaultSuccessMessage: 'Mysteries generated successfully.',
        displayMode: 'modal',
    },
};

function generateItemsSuccess(data, context) {
    const form = context.form;
    const itemType = form.dataset.itemType;
    const config = itemTypeConfigs[itemType];

    if (!config) {
        console.error(`No configuration found for item type "${itemType}"`);
        return;
    }

    const options = {
        defaultSuccessMessage: config.defaultSuccessMessage,
        itemsKey: config.itemsKey,
        listSelector: `.${config.listClass}`,
        listClass: config.listClass,
        itemSelector: config.itemSelector || `.${config.listClass} .${config.itemClass}`,
        itemClass: config.itemClass,
        actionName: config.actionName,
        createItemElement: function(item, index) {
            if (config.displayMode === 'modal') {
                return createItemElement(item, index, config.itemTypeName, config.itemClass, config.actionName);
            } else if (config.displayMode === 'form') {
                return createItemForm(`delete_${config.actionName}`, item, index);
            }
        },
        initItemClickEvents: function(itemClass, actionName) {
            if (config.displayMode === 'modal') {
                initItemClickEvents(itemClass, actionName);
            } else if (config.displayMode === 'form') {
                initItemForms();
            }
        },
        afterItemAdded: function(item, itemIndex, context, options) {
            if (config.displayMode === 'modal') {
                const contentDiv = context.form.closest('.content');
                const modal = createModal(item, itemIndex, config.itemTypeName, config.actionName);
                contentDiv.appendChild(modal);
            }
            // No additional action needed for 'form' display mode
        }
    };

    processItemsSuccess(data, context, options);
}

function processItemsSuccess(data, context, options) {
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
                contentDiv.insertBefore(itemsList, context.form);
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
    const truncatedItem = itemContent.length > 250 ? `${itemContent.substring(0, 250)}...` : itemContent;
    paragraph.textContent = truncatedItem;

    itemElement.appendChild(header);
    itemElement.appendChild(paragraph);

    return itemElement;
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
    Object.values(itemTypeConfigs).forEach(config => {
        if (config.displayMode === 'modal') {
            initItemClickEvents(config.itemClass, config.actionName);
        } else if (config.displayMode === 'form') {
            initItemForms();
        }
    });
}

// Initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize item forms and modals
    if (typeof pageInit === 'function') {
        pageInit();
    }

    // Initialize AJAX for Story Hub forms
    const forms = document.querySelectorAll('form.ajax-form');

    forms.forEach((form) => {
        const errorHandlerName = form.dataset.errorHandler;
        const errorHandler = window[errorHandlerName];

        handleAjaxFormSubmit(form, {
            onSuccess: generateItemsSuccess,
            onError: errorHandler
        });
    });
});