<?php
// Enable Cross-Origin Resource Sharing (CORS) for front-end dashboard accessibility
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type");
header("Content-Type: application/json");

$file_path = "rates.json";

// HANDLE INCOMING PIPELINE WRITES
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $rates_json = $_POST['rates_json'] ?? null;
    $updated_at = filter_input(INPUT_POST, 'updated_at', FILTER_SANITIZE_SPECIAL_CHARS);

    if ($rates_json && $updated_at) {
        $decoded_rates = json_decode($rates_json, true);

        if (is_array($decoded_rates)) {
            $data_to_save = [
                "base" => "USD",
                "rates" => $decoded_rates,
                "updated_at" => $updated_at,
                "last_checked" => date("Y-m-d H:i:s")
            ];

            file_put_contents($file_path, json_encode($data_to_save, JSON_PRETTY_PRINT));
            echo json_encode(["status" => "success", "message" => "USD Base matrix compiled successfully."]);
            exit;
        }
    }
    
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Malformed or empty payload data package."]);
    exit;
}

// HANDLE DASHBOARD FRONTEND DATA REQUESTS
if ($_SERVER["REQUEST_METHOD"] === "GET") {
    if (file_exists($file_path)) {
        echo file_get_contents($file_path);
    } else {
        echo json_encode([
            "base" => "USD",
            "rates" => ["NGN" => 0.00, "BTC" => 0.00, "ETH" => 0.00, "SOL" => 0.00],
            "updated_at" => "Awaiting initial data ingestion stream...",
            "last_checked" => "Never"
        ]);
    }
    exit;
}
?>
