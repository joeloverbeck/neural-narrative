function generateSecretsSuccess(data, context){
    if (data.success) {
        showToast(data.message || 'Secret generated and added to character bio.', 'success');
    } else {
        showToast(data.error || 'An error occurred while generating secret.', 'error');
    }
}