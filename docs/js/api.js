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
  const response = await fetch(`${API_BASE}/api/dvds/`);
  const data = await response.json();
  return data;
}


// ------------------------------------------------------------
//  searchDVDs(query)
//  Hits the search endpoint with a title query string
//  Returns: array of matching DVD objects
// ------------------------------------------------------------
async function searchDVDs(query) {
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
  const response = await fetch(`${API_BASE}/api/dvds/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      title: title,
      purchase_location: purchaseLocation
    })
  });

  if (!response.ok) {
    const error = await response.json();
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

  return true;
}