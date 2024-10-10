// static/index.js

function updateDescription(type) {
    var select = document.getElementById(type + '_name');
    var selectedOption = select.options[select.selectedIndex];
    var description = selectedOption.getAttribute('data-description');
    var descriptionElement = document.getElementById(type + '_description').querySelector('p');
    descriptionElement.innerText = description;
}
window.onload = function() {
    updateDescription('world');
    updateDescription('region');
    updateDescription('area');
}