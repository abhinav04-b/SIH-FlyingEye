const popupButton = document.getElementById('popupButton');
const popup = document.getElementById('popup');
const closeButton = document.getElementById('closeButton');

popupButton.addEventListener('click', () => {
    popup.style.display = 'block';
});

closeButton.addEventListener('click', () => {
    popup.style.display = 'none';
});