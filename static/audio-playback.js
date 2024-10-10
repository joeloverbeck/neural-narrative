// static/audio-playback.js

function playAudio(fileUrl) {
    if (fileUrl && fileUrl !== 'None' && fileUrl !== 'null') {
        var audio = new Audio(fileUrl);
        audio.onerror = function() {
            console.error('Error occurred while loading audio:', audio.error);
            alert('The audio file could not be loaded.');
        };
        audio.play().catch(function(error) {
            console.error('Error occurred while playing audio:', error);
            alert('The audio file couldn\'t be played.');
        });
    } else {
        alert('The RunPod pod isn\'t running.');
    }
}