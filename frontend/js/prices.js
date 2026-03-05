const API_BASE = "http://127.0.0.1:8000";

const cropSelect = document.getElementById("cropSelect");
const marketSelect = document.getElementById("marketSelect");
const refreshBtn = document.getElementById("refreshBtn");

const priceTableBody = document.getElementById("priceTableBody");
const statusText = document.getElementById("statusText");
const lastUpdated = document.getElementById("lastUpdated");

let allPrices = [];
let allCrops = [];
let allMarkets = [];


async function fetchCrops() {
  const res = await fetch(`${API_BASE}/crops`);
  return await res.json();
}

async function fetchMarkets() {
  const res = await fetch(`${API_BASE}/markets`);
  return await res.json();
}

async function fetchLatestPrices() {
  const res = await fetch(`${API_BASE}/prices/latest`);
  return await res.json();
}


function populateDropdown(selectElement, items, labelKey) {
  // Keep first option (All)
  const firstOption = selectElement.querySelector("option");
  selectElement.innerHTML = "";
  selectElement.appendChild(firstOption);

  items.forEach(item => {
    const opt = document.createElement("option");
    opt.value = item.name;
    opt.textContent = item.name;
    selectElement.appendChild(opt);
  });
}


function formatDate(isoString) {
  try {
    const d = new Date(isoString);
    return d.toLocaleString();
  } catch {
    return isoString;
  }
}


function renderTable(prices) {
  priceTableBody.innerHTML = "";

  if (!prices || prices.length === 0) {
    priceTableBody.innerHTML = `
      <tr>
        <td colspan="6" class="text-center text-danger fw-bold">
          No prices found
        </td>
      </tr>
    `;
    return;
  }

  prices.forEach(p => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${p.crop}</td>
      <td>${p.market}</td>
      <td>${p.min}</td>
      <td>${p.max}</td>
      <td><b>${p.modal}</b></td>
      <td>${formatDate(p.updated_at)}</td>
    `;

    priceTableBody.appendChild(row);
  });
}


function applyFilters() {
  const selectedCrop = cropSelect.value;
  const selectedMarket = marketSelect.value;

  let filtered = [...allPrices];

  if (selectedCrop) {
    filtered = filtered.filter(p => p.crop === selectedCrop);
  }

  if (selectedMarket) {
    filtered = filtered.filter(p => p.market === selectedMarket);
  }

  renderTable(filtered);
}


async function refreshPrices() {
  statusText.textContent = "Fetching latest prices...";
  statusText.className = "text-primary fw-bold";

  try {
    allPrices = await fetchLatestPrices();

    statusText.textContent = `Loaded ${allPrices.length} price records`;
    statusText.className = "text-success fw-bold";

    if (allPrices.length > 0) {
      lastUpdated.textContent = formatDate(allPrices[0].updated_at);
    } else {
      lastUpdated.textContent = "--";
    }

    applyFilters();

  } catch (err) {
    console.error(err);
    statusText.textContent = "Backend not reachable. Is FastAPI running?";
    statusText.className = "text-danger fw-bold";
  }
}


async function init() {
  statusText.textContent = "Initializing...";
  statusText.className = "text-primary fw-bold";

  try {
    allCrops = await fetchCrops();
    allMarkets = await fetchMarkets();

    populateDropdown(cropSelect, allCrops, "name");
    populateDropdown(marketSelect, allMarkets, "name");

    statusText.textContent = "Ready. Fetching prices...";
    statusText.className = "text-success fw-bold";

    await refreshPrices();

    // Auto refresh every 15 seconds (frontend refresh)
    setInterval(refreshPrices, 15000);

  } catch (err) {
    console.error(err);
    statusText.textContent = "Error initializing dashboard.";
    statusText.className = "text-danger fw-bold";
  }
}


// Events
cropSelect.addEventListener("change", applyFilters);
marketSelect.addEventListener("change", applyFilters);
refreshBtn.addEventListener("click", refreshPrices);


// Start
init();
