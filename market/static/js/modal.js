// Function to open the modal
function openModal(itemId) {
  console.log("Opening modal for ID:", "modal-" + itemId);
  var modal = document.getElementById("modal-" + itemId);
  console.log("Modal element:", modal);
  if (modal) {
    modal.style.display = "block";
  }
}

// Function to close the modal
function closeModal(itemId) {
  var modal = document.getElementById("modal-" + itemId);
  modal.style.display = "none";
}

// Close the modal if the user clicks outside of it
window.onclick = function (event) {
  if (event.target.classList.contains("modal")) {
    event.target.style.display = "none";
  }
};
