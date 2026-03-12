<?php

$db_host="localhost";
$db_user="root";
$db_pass="";
$db_name="monitoring";

$conn=new mysqli($db_host,$db_user,$db_pass,$db_name);
$conn->set_charset("utf8mb4");

header("Content-Type:application/json");

$action=isset($_GET['action'])?$_GET['action']:'save';

if($action==='last'){
    $result=$conn->query("SELECT id,temperatura,vlaga,vreme FROM senzori ORDER BY id DESC LIMIT 20");
    $rows=[];
    while($row=$result->fetch_assoc()){
        $rows[]=$row;
    }
    echo json_encode(["status"=>"ok", "data"=>array_reverse($rows)]);
}else{
    $temperatura=floatval($_GET['t']);
    $vlaga=floatval($_GET['h']);

    $stmt=$conn->prepare("INSERT INTO senzori (temperatura, vlaga) VALUES (?,?)");
    $stmt->bind_param("dd",$temperatura,$vlaga);
    
    if($stmt->execute()){
        http_response_code(500);
        echo json_encode(["status"=>"ok","id"=>$conn->insert_id]);
    }
    $stmt->close();
}
$conn->close();
?>