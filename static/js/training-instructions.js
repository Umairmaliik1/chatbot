document.addEventListener('DOMContentLoaded', function () { 
    // --- Initialize Quill Editor --- 
    const editor = new Quill('#instructions-editor', { 
        theme: 'snow', 
        placeholder: 'Enter bot instructions here...\n\n# HEADING\nYour content here...', 
        modules: { 
            toolbar: false // No toolbar for a simple textarea-like experience 
        } 
    }); 
 
    const saveButton = document.getElementById('save-instructions-btn'); 
    const originalButtonText = saveButton.innerHTML; 
 
    // --- Load Existing Instructions --- 
    function loadInstructions() { 
        fetch('/api/instructions')
            .then(async response => {
                if (response.status === 401) {
                    showToast('Your session has expired. Please log in again.', 'error');
                    window.location.href = '/login';
                    throw new Error('Session expired'); // Prevent further processing
                }
                if (!response.ok) {
                    let errorMsg = `HTTP Error: ${response.status} ${response.statusText}`;
                    try {
                        const result = await response.json();
                        errorMsg = result.detail || errorMsg;
                    } catch (e) { /* Response not JSON */ }
                    throw new Error(errorMsg);
                }
                return response.json();
            })
            .then(data => {
                editor.setText(data.instructions || '');
            })
            .catch(error => {
                // Don't show an error if it was a session expiry redirect
                if (error.message !== 'Session expired') {
                    console.error('Error loading instructions:', error);
                    const errorMessage = `Error: Could not load instructions. ${error.message}`;
                    editor.setText(errorMessage);
                    showToast(errorMessage, 'error');
                }
            });
    } 
 
    // --- Save Instructions --- 
    saveButton.addEventListener('click', function () { 
        const instructionsText = editor.getText(); 
 
        saveButton.textContent = 'Saving...'; 
        saveButton.disabled = true; 
 
        fetch('/api/instructions', { 
            method: 'POST', 
            headers: { 
                'Content-Type': 'application/json', 
            }, 
            body: JSON.stringify({ instructions: instructionsText }), 
        }) 
        .then(async response => {
            if (response.status === 401) {
                showToast('Your session has expired. Please log in again.', 'error');
                window.location.href = '/login';
                throw new Error('Session expired'); // Prevent further processing
            }
            if (!response.ok) {
                let errorMsg = `HTTP Error: ${response.status} ${response.statusText}`;
                try {
                    const result = await response.json();
                    errorMsg = result.detail || errorMsg;
                } catch (e) { /* Response not JSON */ }
                throw new Error(errorMsg);
            }
            return response.json();
        }) 
        .then(data => showToast(data.message || 'Instructions saved!', 'success')) 
        .catch(error => {
            if (error.message !== 'Session expired') {
                showToast(`Error: ${error.message}`, 'error');
            }
        }) 
        .finally(() => { 
            // Restore button state after a short delay 
            setTimeout(() => { 
                saveButton.innerHTML = originalButtonText; 
                saveButton.disabled = false; 
            }, 1000); 
        }); 
    }); 
 
    // Load instructions when the page is ready 
    loadInstructions(); 
});
