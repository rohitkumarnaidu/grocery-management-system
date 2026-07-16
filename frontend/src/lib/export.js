// frontend/src/lib/export.js
// CSV download helper function - fetches from endpoint and triggers browser download

/**
 * Downloads a CSV file from the specified endpoint and triggers a browser save dialog.
 * @param {string} endpoint - API URL to fetch CSV data from
 * @param {string} filename - target filename for the downloaded file
 */
export async function downloadCsv(endpoint, filename) {
  const response = await fetch(endpoint);
  if (!response.ok) {
    throw new Error(`Failed to download CSV: ${response.statusText}`);
  }
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}
