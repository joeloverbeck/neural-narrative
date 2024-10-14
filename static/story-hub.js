// static/story-hub.js

function pageInit() {
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
}

function openModal(index) {
    document.getElementById('modal-' + index).style.display = 'block';
}

function closeModal(index) {
    document.getElementById('modal-' + index).style.display = 'none';
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

function interestingDilemmasGenerationSuccess(data, context){
    if (data.success){
        showToast(data.message || 'Interesting dilemmas generated.', 'success')
    } else {
        showToast(data.error || 'An error ocurred.', 'error')
    }
}