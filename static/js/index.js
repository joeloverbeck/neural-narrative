// static/index.js

window.onload = function() {
    updateDescription('story_universe');
}

function createPlaythroughSuccess(data, context){
    if (data.success) {
       showToast(data.message || 'Story universe generated successfully', 'success');
       delayedRedirect('/');
    }
    else
    {
        showToast(data.error || 'An error occurred', 'error');
    }
}

function generateStoryUniverseSuccess(data,context){
    if (data.success) {
       showToast(data.message || 'Story universe generated successfully', 'success');
       delayedRedirect('/');
    }
    else
    {
        showToast(data.error || 'An error occurred', 'error');
    }
}

function updateLlmsSuccess(data, context){
    if (data.success) {
       showToast(data.message || 'LLM mappings updated successfully', 'success');
       // Optionally, reload the page or update the UI
    }
    else
    {
        showToast(data.error || 'An error occurred', 'error');
    }
}

document.querySelectorAll('.llm-select').forEach(select => {
    select.addEventListener('change', function() {
        this.classList.add('selected');

        // Remove the class after the animation completes
        setTimeout(() => {
            this.classList.remove('selected');
        }, 500);
    });
});