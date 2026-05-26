const currencyNames = {
    "NGN": "Nigerian Naira", 
    "GHS": "Ghanaian Cedi", 
    "KES": "Kenyan Shilling", 
    "ZAR": "South African Rand", 
    "GBP": "British Pound", 
    "EUR": "Euro", 
    "CAD": "Canadian Dollar",
    "BTC": "Bitcoin", 
    "ETH": "Ethereum", 
    "SOL": "Solana"
};

async function loadRates() {
    const fiatBody = document.getElementById('fiat-table-body');
    const cryptoBody = document.getElementById('crypto-table-body');
    const apiTime = document.getElementById('api-time');
    const syncTime = document.getElementById('sync-time');
    
    try {
        // Fetch dynamic file mapping straight from your PHP server response
        const response = await fetch('../backend/fx-fiat.php');
        const data = await response.json();

        fiatBody.innerHTML = "";
        cryptoBody.innerHTML = "";

        apiTime.textContent = data.updated_at;
        syncTime.textContent = data.last_checked;

        const cryptoKeys = ["BTC", "ETH", "SOL"];

        for (const [currency, value] of Object.entries(data.rates)) {
            const label = currencyNames[currency] || "Alternative Asset";

            if (cryptoKeys.includes(currency)) {
                // Renders formatted coin dollar assets (e.g. $64,250.00)
                const formattedPrice = `$${value.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
                const row = createRow(currency, label, formattedPrice, true);
                cryptoBody.appendChild(row);
            } else {
                // Renders standard decimal units per single US Dollar bill
                const row = createRow(currency, label, value.toFixed(2), false);
                fiatBody.appendChild(row);
            }
        }
    } catch (error) {
        console.error("Dashboard render breakdown:", error);
    }
}

function createRow(code, name, displayValue, isCrypto) {
    const tr = document.createElement('tr');
    const tdName = document.createElement('td');
    tdName.innerHTML = `<span class="badge ${isCrypto ? 'crypto-badge' : ''}">${code}</span> <span style="margin-left: 8px; color: #cbd5e1;">${name}</span>`;      

    const tdRate = document.createElement('td');
    tdRate.className = "rate-value";
    tdRate.textContent = displayValue;

    tr.appendChild(tdName);
    tr.appendChild(tdRate);
    return tr;
}

window.onload = loadRates;
