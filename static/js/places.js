// static/places.js

function generatePlaceSuccessHandler(data, context) {
    const placeType = context.form.dataset.placeType || 'place';
    const placeTypeCapitalized = placeType.charAt(0).toUpperCase() + placeType.slice(1);

    if (data.success) {
        showToast(data.message || `${placeTypeCapitalized} generated successfully`, 'success');
        delayedRedirect('/places');
    } else {
        showToast(data.error || 'An error occurred', 'error');
    }
}

window.onload = function() {
    updateDescription('story_universe');
    updateDescription('world');
    updateDescription('region');
    updateDescription('area');
    updateDescription('location');
}
