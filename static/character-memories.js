document.addEventListener('DOMContentLoaded', function () {
        var selfReflectionContainer = document.querySelector('.self-reflection-container');
        if (selfReflectionContainer) {
            selfReflectionContainer.addEventListener('click', function(event) {
                var fileUrl = event.currentTarget.getAttribute('data-file-url');
                playAudio(fileUrl);
            });
            selfReflectionContainer.style.cursor = 'pointer';
        }
    });