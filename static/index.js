// static/index.js

window.onload = function() {
    updateDescription('story_universe');
}

function generateStoryUniverseSuccess(data,context){
    if (data.success) {
       showToast(data.message || 'Story universe generated successfully', 'success');
        setTimeout(() => {
            window.location.href = '/';
        }, 4000); // Redirects after 4 seconds
    }
    else
    {
        showToast(data.error || 'An error occurred', 'error');
    }
}