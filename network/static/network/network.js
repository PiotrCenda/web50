document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        document.querySelector('.loader').style.display = 'none';
        document.querySelector('.body').style.display = 'flex';
      }, 10);
});