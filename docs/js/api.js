// ============================================================
//  api.js — All communication with the FastAPI backend
//
//  This file is the frontend equivalent of dvd_repo.py.
//  Every function here sends a fetch() request to your API
//  and returns the result.
//
//  Nothing in this file touches the page (no HTML changes).
//  That's app.js's job.
// ============================================================

// The base URL of your FastAPI server.
// Change this if your API runs on a different port.
const API_BASE = "http://192.168.7.199:8000";


// ------------------------------------------------------------
//  getAllDVDs()
//  Replaces: get_all_dvds() from dvd_repo.py
//  Returns: array of DVD objects, e.g. [{id:1, title:"..."}, ...]
// ------------------------------------------------------------
async function getAllDVDs() {
  // fetch() sends an HTTP request — GET is the default method
  const response = await fetch(`${API_BASE}/api/dvds`);

  // .json() reads the response body and converts it to a JS object
  const data = await response.json();
  return data;
}


// ------------------------------------------------------------
//  searchDVDs(query)
//  Hits the search endpoint with a title query string
//  Returns: array of matching DVD objects
// ------------------------------------------------------------
async function searchDVDs(query) {
  // encodeURIComponent handles special characters in the title
  // e.g. "Star Wars" becomes "Star%20Wars" in the URL
  const response = await fetch(`${API_BASE}/api/dvds/search?title=${encodeURIComponent(query)}`);
  const data = await response.json();
  return data;
}


// ------------------------------------------------------------
//  getDVDCount()
//  Returns: { total: 42, message: "You have 42 DVDs..." }
// ------------------------------------------------------------
async function getDVDCount() {
  const response = await fetch(`${API_BASE}/api/dvds/count`);
  const data = await response.json();
  return data;
}


// ------------------------------------------------------------
//  addDVD(title, purchaseLocation)
//  Replaces: insert_dvd() from dvd_repo.py
//  Returns: the newly created DVD object (with its new id)
//           OR throws an error if the request failed
// ------------------------------------------------------------
async function addDVD(title, purchaseLocation) {
  const response = await fetch(`${API_BASE}/api/dvds`, {
    method: "POST",

    // Tell the server we're sending JSON
    headers: {
      "Content-Type": "application/json"
    },

    // JSON.stringify converts a JS object to a JSON string
    // This is what DVDCreate (Pydantic) validates on the backend
    body: JSON.stringify({
      title: title,
      purchase_location: purchaseLocation
    })
  });

  // If the response status is not 2xx (success), throw an error
  // so app.js can show the right message to the user
  if (!response.ok) {
    const error = await response.json();
    // error.detail is the message FastAPI sends from HTTPException
    throw new Error(error.detail || "Failed to add DVD");
  }

  const data = await response.json();
  return data;
}


// ------------------------------------------------------------
//  deleteDVD(id)
//  Replaces: remove_dvd() from dvd_repo.py
//  Returns: nothing (204 No Content on success)
//           OR throws an error if not found
// ------------------------------------------------------------
async function deleteDVD(id) {
  const response = await fetch(`${API_BASE}/api/dvds/${id}`, {
    method: "DELETE"
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to delete DVD");
  }

  // DELETE returns 204 No Content — no body to parse
  return true;
}