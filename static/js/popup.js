document.addEventListener('DOMContentLoaded', function() {
    const closeButton = document.querySelector('.btn-close');
    const modal = document.querySelector('.modal');

    closeButton.addEventListener('click', function() {
        modal.style.display = 'none';
    });
});
