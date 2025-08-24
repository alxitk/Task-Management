document.addEventListener("DOMContentLoaded", function () {
  let selectedUsers = new Set();

  document.querySelectorAll(".user-card.selected").forEach((card) => {
    const userId = parseInt(card.dataset.userId);
    selectedUsers.add(userId);
    const checkbox = card.querySelector('input[type="checkbox"]');
    if (checkbox) checkbox.checked = true;
  });

  const totalUsers = document.querySelectorAll(".user-card").length;
  const totalUsersEl = document.getElementById("total-users");
  if (totalUsersEl) totalUsersEl.textContent = totalUsers;

  const userGrid = document.getElementById("user-grid");
  const selectedUsersEl = document.getElementById("selected-users");
  const selectedSummary = document.getElementById("selected-summary");
  const selectedUsersList = document.getElementById("selected-users-list");

  if (userGrid) {
    function initializeUserCards() {
      const formFields = userGrid.querySelectorAll('input[type="checkbox"]');
      const labels = userGrid.querySelectorAll("label");

      userGrid.innerHTML = "";

      formFields.forEach((input, index) => {
        const label = labels[index];
        if (!label) return;

        const labelText = label.textContent.trim();
        const userId = input.value;

        const userCard = document.createElement("div");
        userCard.className = "user-card";
        userCard.dataset.userId = userId;

        if (input.checked) {
          userCard.classList.add("selected");
        }

        userCard.innerHTML = `
          <div class="user-name">${labelText}</div>
          <div class="user-id">ID: ${userId}</div>
          ${input.outerHTML}
        `;

        const hiddenInput = userCard.querySelector("input");
        hiddenInput.style.display = "none";

        userCard.addEventListener("click", function () {
          toggleUserSelection(this, hiddenInput);
        });

        userGrid.appendChild(userCard);
      });

      updateStats();
      updateSelectedSummary();
    }

    function toggleUserSelection(card, input) {
      const wasSelected = card.classList.contains("selected");

      if (wasSelected) {
        card.classList.remove("selected");
        input.checked = false;
      } else {
        card.classList.add("selected", "just-selected");
        input.checked = true;

        setTimeout(() => {
          card.classList.remove("just-selected");
        }, 300);
      }

      updateStats();
      updateSelectedSummary();
    }

    function updateStats() {
      const allCards = userGrid.querySelectorAll(".user-card");
      const selectedCards = userGrid.querySelectorAll(".user-card.selected");

      if (totalUsersEl) totalUsersEl.textContent = allCards.length;
      if (selectedUsersEl) selectedUsersEl.textContent = selectedCards.length;
    }

    function updateSelectedSummary() {
      const selectedCards = userGrid.querySelectorAll(".user-card.selected");

      if (selectedCards.length > 0 && selectedSummary) {
        selectedSummary.classList.add("show");
        if (selectedUsersList) {
          selectedUsersList.innerHTML = "";

          selectedCards.forEach((card) => {
            const userName = card.querySelector(".user-name").textContent;
            const userId = card.dataset.userId;

            const tag = document.createElement("div");
            tag.className = "selected-user-tag";
            tag.innerHTML = `${userName} <span style="opacity: 0.7;">(${userId})</span>`;

            selectedUsersList.appendChild(tag);
          });
        }
      } else if (selectedSummary) {
        selectedSummary.classList.remove("show");
      }
    }

    initializeUserCards();
  }
});