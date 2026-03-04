<?php
// =====================================================
// save_data.php - Прием и снимање на сензорски податоци
// Паметна работна станица - PHP Backend Скрипта
// =====================================================

// --- Конфигурација на база на податоци ---
$db_host = "localhost";
$db_user = "root";       // Корисник (промени ако е потребно)
$db_pass = "";           // Лозинка (промени ако е потребно)
$db_name = "monitoring";

// --- Конекција со MySQL база ---
$conn = new mysqli($db_host, $db_user, $db_pass, $db_name);
$conn->set_charset("utf8mb4");

if ($conn->connect_error) {
    http_response_code(500);
    die(json_encode(["status" => "error", "message" => "Конекција неуспешна: " . $conn->connect_error]));
}

header("Content-Type: application/json");

// -------------------------------------------------------
// GET /save_data.php?t=23.5&h=55.3  → Снимање на нов запис
// GET /save_data.php?action=last     → Враќање на последни 20 записи
// -------------------------------------------------------

$action = isset($_GET['action']) ? $_GET['action'] : 'save';

if ($action === 'last') {
    // --- Враќање на последни 20 мерења ---
    $result = $conn->query("SELECT id, temperatura, vlaga, vreme FROM senzori ORDER BY id DESC LIMIT 20");
    $rows = [];
    while ($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }
    echo json_encode(["status" => "ok", "data" => array_reverse($rows)]);

} else {
    // --- Снимање на ново мерење ---
    if (!isset($_GET['t']) || !isset($_GET['h'])) {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Недостасуваат параметри t и h"]);
        exit;
    }

    $temperatura = floatval($_GET['t']);
    $vlaga       = floatval($_GET['h']);

    // Валидација на вредности
    if ($temperatura < -40 || $temperatura > 80 || $vlaga < 0 || $vlaga > 100) {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Невалидни вредности"]);
        exit;
    }

    $stmt = $conn->prepare("INSERT INTO senzori (temperatura, vlaga) VALUES (?, ?)");
    $stmt->bind_param("dd", $temperatura, $vlaga);

    if ($stmt->execute()) {
        echo json_encode(["status" => "ok", "id" => $conn->insert_id]);
    } else {
        http_response_code(500);
        echo json_encode(["status" => "error", "message" => $stmt->error]);
    }
    $stmt->close();
}

$conn->close();
?>
