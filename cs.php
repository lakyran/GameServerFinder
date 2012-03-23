<?php

function jsonOutput($query){
	$jsonString = "[";
	$ofirst = true;
	while ($row = $query->fetchArray(SQLITE3_ASSOC)){
		if($ofirst){
			$ofirst = false;
		}
		else{
			$jsonString = $jsonString . ",\n";
		}
		$first = true;
		$jsonString = $jsonString . "{";
		foreach ($row as $key => $value){
			if($first){
				$first = false;
			}
			else{
				$jsonString = $jsonString . ",";
			}
			$jsonString = $jsonString . '"'.$key.'"' . ': "' . $value . '"';
		}
		$jsonString = $jsonString . "}";
	}
	$jsonString = $jsonString . "]";
	return $jsonString;
}

$db = new SQLite3("./db/csdb.sqlite");
$result = $db->query("select * from cs");
$jsonString = jsonOutput($result);
echo $jsonString;

?>
