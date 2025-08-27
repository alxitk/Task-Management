document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM loaded");

  const selectBtn = document.getElementById("assignees-select");
  const dropdown = document.getElementById("assignees-dropdown");

  console.log("Select button:", selectBtn);
  console.log("Dropdown:", dropdown);

  if (selectBtn) {
    selectBtn.addEventListener("click", function (e) {
      console.log("Button clicked!");
      e.preventDefault();

      if (dropdown) {
        console.log("Toggling dropdown");
        dropdown.classList.toggle("hide");
        selectBtn.classList.toggle("open");
      } else {
        console.log("Dropdown not found!");
      }
    });
  } else {
    console.log("Select button not found!");
  }
});