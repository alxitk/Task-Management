document.addEventListener("DOMContentLoaded", function () {
  const logoutLink = document.getElementById("logout-link");
  if (logoutLink) {
    logoutLink.addEventListener("click", function (e) {
      e.preventDefault();
      const logoutForm = document.getElementById("logout-form");
      if (logoutForm) {
        logoutForm.submit();
      }
    });
  }
});