# Global Asset Monitor

A full-stack, real-time financial data platform that aggregates global fiat exchange rates and top cryptocurrency valuations benchmarked against the US Dollar ($1 USD Base). The system employs a decoupled architecture consisting of an automated Python data ingestion script, a persistent PHP data caching gateway, and an asynchronous, lightweight JavaScript user dashboard.

## 🏗️ System Architecture & Data Flow

1. **Extraction (Python)**: An active automated routine pulls live fiat tables and crypto pricing frameworks from web APIs, standardizes the currency baselines, and bundles them into serialized matrix structures.
2. **Ingestion & Storage (PHP)**: A dedicated dual-method API gateway endpoint processes incoming multi-part pipeline streams via `POST`, decodes the payload parameters, and caches them to a local JSON structure to maximize system performance and mitigate API rate limiting.
3. **Consumption & Rendering (JS)**: The user interface triggers asynchronous network fetch requests via `GET` handlers to dynamically update components in the DOM tree every 30 seconds without full-page reloads.

## 🚀 Key Features

* **Automated Python Pipeline**: Custom data collection worker using native Python standard libraries (`urllib`) with integrated User-Agent rotation to bypass connection drops.
* **Dual Asset Monitoring Matrix**: Simultaneously tracks 7 major global fiat currencies (`NGN`, `GHS`, `KES`, `ZAR`, `GBP`, `EUR`, `CAD`) and top crypto utility tokens (`BTC`, `ETH`, `SOL`).
* **Persistent Local Cache Engine**: Caches live asset price frames into structured `rates.json` payloads on the file server to optimize read throughput and bypass third-party rate limits.
* **Bi-directional API Gateway**: Features a single-endpoint PHP controller that cleanly isolates backend streaming writes (`POST`) from client-side UI requests (`GET`).
* **Dynamic Localized Formatting**: Native frontend rendering engines map custom currency badges and format numerical streams into human-readable currency strings (e.g., `$64,250.00`).

## 🛠️ Technical Stack

* **Data Pipeline**: Python 3.x (`json`, `urllib.request`, `urllib.parse`, `time`).
* **Backend API Gateway**: Core PHP 8.x Engine.
* **Frontend UI**: Semantic HTML5, CSS3 Custom Properties, Vanilla JavaScript (ES6, Fetch API, DOM Manipulation).
* **Storage Component**: Local JSON-serialized schema model file (`rates.json`).

## 🗂️ Project Structure

```text
├── assets/
│   ├── css/
│   │   └── fx-fiat-style.css   # Layout layout structure & component style tokens
│   └── js/
│   │   └── fx-fiat-app.js      # Core client data rendering pipeline
├── backend/
│   ├── fx-fiat.php             # Unified POST ingest / GET egress server gateway
│   └── rates.json              # Local persistent JSON asset database
├── pipeline/
│   └── scraper.py              # Automated live data extraction pipeline script
└── index.html                  # Core presentation layer user interface dashboard
```

## 🔌 API Gateway Specifications

### 1. External Ingestion (Pipeline Stream)
* **Method**: `POST`
* **Endpoint**: `/backend/fx-fiat.php`
* **Form Parameters**:
  * `rates_json` (string): Stringified JSON object containing active key-value mappings (e.g., `{"NGN":1600.50, "BTC":64250.00}`).
  * `updated_at` (string): Remote source time signature string.

### 2. Client Ingress (Frontend Requests)
* **Method**: `GET`
* **Endpoint**: `/backend/fx-fiat.php`
* **Expected Response Output**:
  ```json
  {
    "base": "USD",
    "rates": {
      "NGN": 1602.50,
      "BTC": 64250.00,
      "ETH": 3450.25,
      "SOL": 145.10
    },
    "updated_at": "Tue, 26 May 2026 14:30:00 UTC",
    "last_checked": "2026-05-26 15:35:12"
  }
  ```

## ⚙️ Local Deployment Guide

### Step 1: Clone the Application
```bash
git clone https://github.com
cd global-asset-monitor
```

### Step 2: Spin Up the Web Server
Ensure your project path is served out of a valid PHP evaluation layer. You can start the native PHP server component directly out of your workspace root directory:
```bash
php -S localhost:80
```
*(Note: If you run your server out of a custom virtual directory path, make sure to update the `backend_url` string in your Python pipeline file to point to your new route).*

### Step 3: Trigger the Data Pipeline
In a separate terminal tab, spin up the background worker thread to pull financial metrics and stream them directly into your local database:
```bash
python pipeline/scraper.py
```

### Step 4: Access the Dashboard
Open your choice of browser engine and load up `http://localhost:80/index.html` to observe the system handling records on a 5-second backend refresh cycle.

## 🔮 Future Roadmap (AI Integration Blueprint)

Designed with clear architectural boundaries, this data hub is primed for upstream machine learning capabilities:
* **Predictive Volatility Pipelines**: Appending automated Python micro-routines running `Scikit-Learn` or `LSTMs` to forecast the next 24-hour rate bands directly on incoming payloads.
* **Natural Language Processing (NLP) Layer**: Integrating small open-source transformer models (via an AI endpoint) allowing users to type natural queries like *"Which currency is recovering fastest against the USD today?"* and generating automated data text briefs.
* **Anomalous Drift Detection**: Implementing isolation forest checks inside the Python extraction loop to automatically catch, flag, and suppress sudden corrupted data feed jumps before they hit database levels.
