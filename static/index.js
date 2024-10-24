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