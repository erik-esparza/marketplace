// Function to open the modal
function openModal(itemId) {
  var modal = document.getElementById("modal-" + itemId);
  modal.style.display = "block";
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

// Function to open the modal of purchase confirmation
function openModalPurchase(itemId) {
  console.log("Opening modal for ID:", "modal-purchase-" + itemId);
  var modal = document.getElementById("modal-purchase-" + itemId);
  console.log("Modal element:", modal);
  if (modal) {
    modal.style.display = "block";
  }
}

function closeModalPurchase(itemId) {
  var modal = document.getElementById("modal-purchase-" + itemId);
  modal.style.display = "none";
}

function openModalSale(itemId) {
  console.log("Opening modal for ID:", "modal-sale-" + itemId);
  var modal = document.getElementById("modal-sale-" + itemId);
  console.log("Modal element:", modal);
  if (modal) {
    modal.style.display = "block";
  }
}

function closeModalSale(itemId) {
  var modal = document.getElementById("modal-sale-" + itemId);
  modal.style.display = "none";
}
