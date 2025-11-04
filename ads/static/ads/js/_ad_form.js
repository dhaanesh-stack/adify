  document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.getElementById("id_category");
    const eventDateContainer = document.getElementById("event-date-container");

    function toggleEventDate() {
      const selectedText = categorySelect.options[categorySelect.selectedIndex]?.text?.toLowerCase();
      if (selectedText && selectedText.includes("event")) {
        eventDateContainer.classList.remove("hidden");
      } else {
        eventDateContainer.classList.add("hidden");
      }
    }

    toggleEventDate();
    categorySelect.addEventListener("change", toggleEventDate);
  });
