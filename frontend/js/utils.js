// ============================================================
//  utils.js — Small helper functions
//
//  These don't talk to the API or touch the page directly.
//  They're just reusable utilities that app.js can call.
// ============================================================


// ------------------------------------------------------------
//  formatDate(dateString)
//  Converts "2025-01-15" → "Jan 15, 2025"
// ------------------------------------------------------------
function formatDate(dateString) {
  if (!dateString) return "Unknown date";

  // new Date() converts a date string into a JavaScript Date object
  const date = new Date(dateString);

  // toLocaleDateString formats it as a readable string
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric"
  });
}


// ------------------------------------------------------------
//  showMessage(elementId, text, type)
//  Displays a success or error message under the add form
//  type: "success" or "error"
// ------------------------------------------------------------
function showMessage(elementId, text, type) {
  const el = document.getElementById(elementId);

  el.textContent = text;

  // Remove both classes first, then add the right one
  el.classList.remove("hidden", "success", "error");
  el.classList.add(type);

  // Automatically hide the message after 4 seconds
  setTimeout(() => {
    el.classList.add("hidden");
  }, 4000);
}


// ------------------------------------------------------------
//  clearInputs(...ids)
//  Clears the value of multiple input fields at once
// ------------------------------------------------------------
function clearInputs(...ids) {
  ids.forEach(id => {
    document.getElementById(id).value = "";
  });
}