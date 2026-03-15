// ============================================================
//  app.js — Main application logic
//
//  This file:
//  1. Renders DVD cards onto the page
//  2. Handles the Add button click
//  3. Handles the Search input
//  4. Updates the DVD count in the header
//
//  It uses functions from api.js (fetch calls) and
//  utils.js (helpers) — that's why they load first in index.html
// ============================================================


// ------------------------------------------------------------
//  renderDVDs(dvds)
//  Takes an array of DVD objects from the API and builds
//  the HTML cards on the page.
// ------------------------------------------------------------
function renderDVDs(dvds) {
  // Get the grid container element from the HTML
  const grid = document.getElementById("dvd-grid");

  // If the collection is empty, show a friendly message
  if (dvds.length === 0) {
    grid.innerHTML = `
      <div class="empty-state">
        <span class="empty-icon">📀</span>
        No DVDs found. Add one above!
      </div>
    `;
    return;
  }

  // Build one card per DVD and join them into one big HTML string.
  // map() loops through every dvd in the array and returns a card string.
  // join("") stitches all the card strings together with no separator.
  grid.innerHTML = dvds.map(dvd => `
    <div class="dvd-card">
      <div class="dvd-title">${dvd.title}</div>
      <div class="dvd-meta">
        <span class="dvd-location">${dvd.purchase_location || "Unknown location"}</span>
        <span class="dvd-date">${formatDate(dvd.purchase_date)}</span>
      </div>
      <div class="dvd-card-footer">
        <button
          class="btn btn-delete"
          onclick="handleDelete(${dvd.id}, '${dvd.title.replace(/'/g, "\\'")}')">
          Remove
        </button>
      </div>
    </div>
  `).join("");
}


// ------------------------------------------------------------
//  updateCount()
//  Fetches the DVD count from the API and updates the header badge
// ------------------------------------------------------------
async function updateCount() {
  const data = await getDVDCount();
  document.getElementById("dvd-count").textContent = `${data.total} DVDs`;
}


// ------------------------------------------------------------
//  loadCollection()
//  Fetches all DVDs and renders them — called on page load
// ------------------------------------------------------------
async function loadCollection() {
  const dvds = await getAllDVDs();
  renderDVDs(dvds);
  updateCount();

  // Update the section title
  document.getElementById("collection-title").textContent = "Collection";
}


// ------------------------------------------------------------
//  handleAdd()
//  Called when the "Add to Collection" button is clicked.
//  Reads the input fields, calls addDVD(), and refreshes the page.
// ------------------------------------------------------------
async function handleAdd() {
  // Grab what the user typed in the input boxes
  const title = document.getElementById("input-title").value.trim();
  const location = document.getElementById("input-location").value.trim();

  // Basic validation — don't bother the API with empty inputs
  if (!title) {
    showMessage("add-message", "Please enter a movie title.", "error");
    return;
  }

  if (!location) {
    showMessage("add-message", "Please enter where you got it.", "error");
    return;
  }

  // Disable the button while the request is running
  // so the user can't accidentally click it twice
  const btn = document.getElementById("add-btn");
  btn.disabled = true;
  btn.textContent = "Adding...";

  // try/catch handles errors from the API (e.g. duplicate title)
  try {
    await addDVD(title, location);

    // Success — clear the inputs and show a success message
    clearInputs("input-title", "input-location");
    showMessage("add-message", `"${title}" was added to your collection!`, "success");

    // Reload the full collection so the new DVD appears
    await loadCollection();

  } catch (error) {
    // The error message comes from FastAPI's HTTPException detail
    showMessage("add-message", error.message, "error");
  }

  // Re-enable the button either way
  btn.disabled = false;
  btn.textContent = "Add to Collection";
}


// ------------------------------------------------------------
//  handleDelete(id, title)
//  Called when a Remove button on a DVD card is clicked.
// ------------------------------------------------------------
async function handleDelete(id, title) {
  // Confirm before deleting — always a good idea!
  const confirmed = confirm(`Remove "${title}" from your collection?`);
  if (!confirmed) return;

  try {
    await deleteDVD(id);

    // Reload the collection so the card disappears
    await loadCollection();

  } catch (error) {
    alert("Could not remove DVD: " + error.message);
  }
}


// ------------------------------------------------------------
//  handleSearch(query)
//  Called on every keystroke in the search input (oninput in HTML)
// ------------------------------------------------------------
async function handleSearch(query) {
  // If the search box is cleared, reload the full collection
  if (query.trim() === "") {
    loadCollection();
    return;
  }

  // Search the API and render whatever comes back
  const results = await searchDVDs(query);
  renderDVDs(results);

  // Update the section title to show search context
  document.getElementById("collection-title").textContent =
    `Results for "${query}" (${results.length})`;
}


// ------------------------------------------------------------
//  Page load — this runs automatically when the page opens
//  It's the equivalent of your CLI's main() function
// ------------------------------------------------------------
loadCollection();