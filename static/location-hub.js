// static/location-hub.js

document.addEventListener('DOMContentLoaded', function () {
        var placeDescription = document.querySelector('.place-description');
        if (placeDescription) {
            placeDescription.addEventListener('click', function(event) {
                var fileUrl = event.currentTarget.getAttribute('data-file-url');
                playAudio(fileUrl);
            });
            placeDescription.style.cursor = 'pointer';
        }
    });