document.addEventListener('DOMContentLoaded', function() {
    const settingsForm = document.getElementById('settings-form');
    if (!settingsForm) return;

    const saveButton = settingsForm.querySelector('.btn-save');

    settingsForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const originalButtonText = saveButton.textContent;
        saveButton.textContent = 'Saving...';
        saveButton.disabled = true;

        const formData = new FormData(settingsForm);
        const data = Object.fromEntries(formData.entries());

        // Basic client-side validation for password
        if (data.new_password && data.new_password !== data.confirm_password) {
            showToast('Passwords do not match.', 'error');
            saveButton.textContent = originalButtonText;
            saveButton.disabled = false;
            return;
        }
        
        if (data.new_password && data.new_password.length < 8) {
            showToast('Password must be at least 8 characters long.', 'error');
            saveButton.textContent = originalButtonText;
            saveButton.disabled = false;
            return;
        }

        // Convert chat_rate to a float, or null if empty
        data.chat_rate = data.chat_rate ? parseFloat(data.chat_rate) : null;

        fetch('/api/settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        })
        .then(response => response.json().then(body => ({ ok: response.ok, body })))
        .then(({ ok, body }) => {
            if (!ok) throw new Error(body.detail || 'Failed to save settings.');
            showToast(body.message, 'success');
            document.getElementById('new_password').value = '';
            document.getElementById('confirm_password').value = '';
        })
        .catch(error => showToast(error.message, 'error'))
        .finally(() => {
            saveButton.textContent = originalButtonText;
            saveButton.disabled = false;
        });
    });
});