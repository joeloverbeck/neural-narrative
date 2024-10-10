// static/story-hub.js

document.addEventListener('DOMContentLoaded', function() {
    // Fade-out effect for items
    const itemForms = document.querySelectorAll('.item-form');
    itemForms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const itemButton = form.querySelector('.post-it');
            itemButton.classList.add('fade-out');
            setTimeout(function() {
                form.submit();
            }, 500);
        });
    });
});