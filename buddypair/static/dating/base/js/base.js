function toggleFloatingNotification(){
    const floatnotification = document.getElementById("floatingnotification");
    const menuIcon = document.querySelector(".icon-container.menu");
    floatnotification.classList.add('show');
}
document.querySelectorAll('.close-btn').forEach(function(button) {
    button.addEventListener('click', function() {
      this.parentElement.style.display = 'none';
    });
  });