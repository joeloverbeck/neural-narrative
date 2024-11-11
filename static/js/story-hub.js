// static/story-hub.js

// Configuration object for different item types
const itemTypeConfigs = {
    antagonist: {
        itemTypeName: 'Antagonist',
        itemsKey: 'antagonists',
        actionName: 'antagonist',
        iconClass: 'fa-solid fa-skull',
        defaultSuccessMessage: 'Antagonists generated successfully.',
    },
    plot_blueprint: {
        itemTypeName: 'Plot Blueprint',
        itemsKey: 'plot_blueprints',
        actionName: 'plot_blueprint',
        iconClass: 'fas fa-lightbulb',
        defaultSuccessMessage: 'Plot blueprints generated successfully.',
    },
    scenario: {
        itemTypeName: 'Scenario',
        itemsKey: 'scenarios',
        actionName: 'scenario',
        defaultSuccessMessage: 'Scenarios generated successfully.',
    },
    artifact: {
        itemTypeName: 'Artifact',
        itemsKey: 'artifacts',
        actionName: 'artifact',
        iconClass: 'fas fa-gem',
        defaultSuccessMessage: 'Artifacts generated successfully.',
    },
    dilemma: {
        itemTypeName: 'Dilemma',
        itemsKey: 'dilemmas',
        actionName: 'dilemma',
        defaultSuccessMessage: 'Dilemmas generated successfully.',
    },
    goal: {
        itemTypeName: 'Goal',
        itemsKey: 'goals',
        actionName: 'goal',
        defaultSuccessMessage: 'Goals generated successfully.',
    },
    lore_or_legend: {
        itemTypeName: 'Lore or Legend',
        itemsKey: 'lore_and_legends',
        actionName: 'lore_or_legend',
        iconClass: 'fas fa-dragon',
        defaultSuccessMessage: 'Lore and legends generated successfully.',
    },
    plot_twist: {
        itemTypeName: 'Plot Twist',
        itemsKey: 'plot_twists',
        actionName: 'plot_twist',
        defaultSuccessMessage: 'Plot twists generated successfully.',
    },
    mystery: {
        itemTypeName: 'Mystery',
        itemsKey: 'mysteries',
        actionName: 'mystery',
        iconClass: 'fas fa-puzzle-piece',
        defaultSuccessMessage: 'Mysteries generated successfully.',
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
        actionName: config.actionName,
        createItemElement: function(item, index) {
            return createItemElement(item, index, config.itemTypeName, config.actionName);
        },
        initItemClickEvents: function(actionName) {
            initItemClickEvents(actionName);
        },
        afterItemAdded: function(item, itemIndex, context, options) {
            const contentDiv = context.form.closest('.content');
            const modal = createModal(item, itemIndex, config.itemTypeName, config.actionName);
            contentDiv.appendChild(modal);
        }
    };

    processItemsSuccess(data, context, options);
}

    function processItemsSuccess(data, context, options) {
    if (data.success) {
        showToast(data.message || options.defaultSuccessMessage, 'success');

        if (data[options.itemsKey]) {
            let contentDiv = context.form.closest('.content');
            let itemsList = contentDiv.querySelector('.items-list');

            // Determine number of items to know what modal should be opened.
            const existingItems = itemsList ? itemsList.querySelectorAll('.item') : [];
            const startIndex = existingItems.length;

            if (!itemsList) {
                itemsList = document.createElement('div');
                itemsList.classList.add('items-list');
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
                options.initItemClickEvents(options.actionName);
            }
        }
    } else {
        showToast(data.error || 'An error occurred', 'error');
    }
}


function openModal(index, conceptType) {
    document.getElementById(`modal-${conceptType}-${index}`).style.display = "block";
}

function closeModal(index, conceptType) {
    document.getElementById(`modal-${conceptType}-${index}`).style.display = "none";
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
    modalContent.appendChild(p);
    modalContent.appendChild(form);

    modal.appendChild(modalContent);

    return modal;
}

function createItemElement(itemContent, index, itemType, actionName) {
    const itemElement = document.createElement('div');
    itemElement.classList.add('item');
    itemElement.setAttribute('data-index', index);
    itemElement.setAttribute('data-action-name', actionName);

    itemElement.onclick = function() {
        openModal(index, actionName);
    };

    const paragraph = document.createElement('p');
    const truncatedItem = itemContent.length > 250 ? itemContent.substring(0, 250) + '...' : itemContent;
    paragraph.textContent = truncatedItem;

    itemElement.appendChild(paragraph);

    return itemElement;
}

function initItemClickEvents(actionName) {
    const items = document.querySelectorAll(`.item[data-action-name="${actionName}"]`);

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

function pageInit() {
    Object.values(itemTypeConfigs).forEach(config => {
        initItemClickEvents(config.actionName);
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