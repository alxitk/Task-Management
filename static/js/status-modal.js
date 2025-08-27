document.addEventListener("DOMContentLoaded", function () {
  const overlay = document.getElementById("status-overlay");
  const openBtn = document.getElementById("change-status-btn");
  const closeBtn = document.getElementById("close-status-btn");

  function openStatusModal() {
    if (overlay) overlay.style.display = "block";
  }

  function closeStatusModal() {
    if (overlay) overlay.style.display = "none";
  }

  if (openBtn) openBtn.addEventListener("click", openStatusModal);
  if (closeBtn) closeBtn.addEventListener("click", closeStatusModal);

  if (overlay) {
    overlay.addEventListener("click", function (e) {
      if (e.target === this) closeStatusModal();
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeStatusModal();
  });
});