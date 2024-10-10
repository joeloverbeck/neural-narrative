// static/collapsible.js

document.addEventListener('DOMContentLoaded', function() {
    // Collapsible sections
    const collapsibles = document.querySelectorAll('.collapsible');
    collapsibles.forEach(function(collapsible) {
        collapsible.addEventListener('click', function() {
            this.classList.toggle('active');
            const content = this.nextElementSibling;
            if (content.style.display === 'block') {
                content.style.display = 'none';
            } else {
                content.style.display = 'block';
            }
        });

        // On load: Display content for any collapsible that has 'active' class
        if (collapsible.classList.contains('active')) {
            const content = collapsible.nextElementSibling;
            content.style.display = 'block';
        }
    });
});