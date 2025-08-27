function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) {
        console.error('Toast container not found!');
        return;
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    // Animate in
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);

    // Automatically remove after a few seconds
    setTimeout(() => {
        toast.classList.remove('show');
        // Remove the element from the DOM after the fade-out animation
        toast.addEventListener('transitionend', () => {
            toast.remove();
        });
    }, 4000);
}