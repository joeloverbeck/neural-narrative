function resolveSelfReflectionSuccess(data, context) {
    if (data.success) {
        showToast(data.message || 'Self-reflection generated successfully.', 'success');

        // Update the self-reflection-container
        const container = document.getElementById('self-reflection-container');
        if (container) {
            // Update the data-file-url attribute
            container.setAttribute('data-file-url', data.self_reflection_voice_line_url);

            // Update the content with the self_reflection_text
            container.innerHTML = `
                <p>${data.self_reflection_text}</p>
                <i class="fas fa-play play-icon"></i>
                <div class="waveform">
                    <div></div>
                    <div></div>
                    <div></div>
                    <div></div>
                    <div></div>
                </div>`;

            // Re-initialize the audio playback for this element
            container.classList.remove('audio-initialized');
            initAudioPlayback();
            }
    } else {
        showToast(data.error || 'An error occurred while generating self-reflection.', 'error');
    }
}