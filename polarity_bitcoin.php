<?php
$serverName = "scrapersmsda2017.database.windows.net";
$connectionOptions = array(
 "Database" => "msdatwitter",
 "Uid" => "scrapersmsda",
 "PWD" => "msdascrapers@2017"
);
//Establishes the connection
$conn = sqlsrv_connect($serverName, $connectionOptions);
$keywords = $_GET['keyword'];
//Select Query
$tsql= "select count(*) as polarity_count,  polarity from twitterData_modified where keywords like '%".$keywords."%' group by polarity";
//echo $tsql;
//Executes the query
$getResults= sqlsrv_query($conn, $tsql);
//Error handling
if ($getResults == FALSE)
 die(FormatErrors(sqlsrv_errors()));
?>
<h1> Results : </h1>
<?php

$posCount =0;
$negCount =0;
$neutralCount = 0;
$counts = array($posCount,$negCount, $neutralCount);
//echo($posCount ." ***** ". $negCount." **** ". " ***** ". $neutralCount);
while ($row = sqlsrv_fetch_array($getResults, SQLSRV_FETCH_ASSOC)) {
	//print_r($row);
	//echo($row['polarity_count']);
	//echo("<br>");
	//echo($row['polarity']);
	//echo("<br>");
	//if($row['Keywords'] == "bitcoin, crypto currency" )
	//{
		if($row['polarity'] == "+")
		{
			$posCount = $row['polarity_count'];
		}
		else if($row['polarity'] == "-")
		{
			$negCount = $row['polarity_count'];
		}
		else
		{
			$neutralCount = $row['polarity_count'];
		}
	//}
}

//echo($posCount ." ***** ". $negCount." **** ". " ***** ". $neutralCount);
//echo(max($posCount,$negCount, $neutralCount));
//echo('<br>');
/**echo(min($posCount,$negCount, $neutralCount));**/
sqlsrv_free_stmt($getResults);
function FormatErrors( $errors )
{
 /* Display errors. */
 echo "Error information: <br/>";
 foreach ( $errors as $error )
 {
 echo "SQLSTATE: ".$error['SQLSTATE']."<br/>";
 echo "Code: ".$error['code']."<br/>";
 echo "Message: ".$error['message']."<br/>";
 }
}
?>

<?php
 
$dataPoints = array(
	array("label"=> "Positvie", "y"=> $posCount, color => '#66BE03'),
	array("label"=> "Negative", "y"=> $negCount, color => '#FC0303'),
	array("label"=> "Neutral", "y"=> $neutralCount, color => '#024EFC')
);
//print_r($dataPoints);
//$labels=array("+","-",".");
//echo $labels[0];

/**
// PHP Data Objects(PDO) Sample Code:
try {
    $conn = new PDO("sqlsrv:server = tcp:scrapersmsda2017.database.windows.net,1433; Database = msdatwitter", "scrapersmsda", "msdascrapers@2017");
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    print("Connection was established")
}
catch (PDOException $e) {
    print("Error connecting to SQL Server.");
    die(print_r($e));
}**/

 
?>
<!DOCTYPE HTML>
<html>
<head>
<meta http-equiv="refresh" content="3">
<script>
window.onload = function () {

var title = <?php echo json_encode("Polarity Count for topic ".$keywords);?>;
var chart = new CanvasJS.Chart("chartContainer", {
	title: {
		text: title
	},
	axisY: {
		minimum: 0,
		maximum: <?php echo(max($posCount,$negCount, $neutralCount) + 100);?>,
		suffix: ""
	},
	data: [{
		type: "column",
		yValueFormatString: "#,##0",
		indexLabel: "{y}",
		dataPoints: <?php echo json_encode($dataPoints, JSON_NUMERIC_CHECK); ?>
	}]
});
 
function updateChart() {
/**<?php
	//Select Query
	$tsql= "select count(*) as polarity_count,  polarity from twitterData_modified where keywords like '%bitcoin%' group by polarity";
	//Executes the query
	$getResults= sqlsrv_query($conn, $tsql);
	//Error handling
	if ($getResults == FALSE)
	 die(FormatErrors(sqlsrv_errors()));
	//echo("<br>entered<br>");
	$posCount1 =0;
	$negCount1 =0;
	$neutralCount1 = 0;
	//$counts = array($posCount,$negCount, $neutralCount);
        $tsql_recurring= "select count(*) as polarity_count,polarity from twitterData_modified where keywords like '%bitcoin%' group by polarity";
	$getResults= sqlsrv_query($conn, $tsql_recurring);
?>
	console.log(<?php echo json_encode($getResults, SQLSRV_FETCH_ASSOC);?>);
	//echo(max($posCount,$negCount, $neutralCount));
	//echo('<br>');
<?php
	//Error handling
	if ($getResults == FALSE)
	 die(FormatErrors(sqlsrv_errors()));

	while ($row = sqlsrv_fetch_array($getResults, SQLSRV_FETCH_ASSOC)) {
?>
	console.log(<?php echo json_encode($row);?>);
	//echo(max($posCount,$negCount, $neutralCount));
	//echo('<br>');
<?php
	//	if($row['Keywords'] == "bitcoin, crypto currency" )
	//	{
			if($row['polarity'] == "+")
			{
				$posCount1 = $row['polarity_count'];
			}
			else if($row['polarity'] == "-")
			{
				$negCount1 = $row['polarity_count'];
			}
			else
			{
				$neutralCount1 = $row['polarity_count'];
			}
	//	}
	}
?>
	console.log(<?php echo json_encode($posCount1 ." ***** ". $negCount1." **** ". " ***** ". $neutralCount1);?>);
	//echo(max($posCount,$negCount, $neutralCount));
	//echo('<br>');
<?php
	$dataPoints_modified = array(
	array("label"=> "Positvie", "y"=> $posCount1, color => '#66BE03'),
	array("label"=> "Negative", "y"=> $negCount1, color => '#FC0303'),
	array("label"=> "Neutral", "y"=> $neutralCount1, color => '#024EFC')
	);

	
?>**/
	var color,deltaY, yVal;
	var dps = <?php echo json_encode($dataPoints, JSON_NUMERIC_CHECK); ?>;
	console.log(dps);
console.log(<?php echo $posCount1;?>);
	//window.alert(dps);
	for (var i = 0; i < dps.length; i++) {
		yVal =  dps[i].y;
		//color = yVal > 75 ? "#FF2500" : yVal >= 50 ? "#FF6000" : yVal < 50 ? "#41CF35" : null;
		//labelName = <?php echo($labels[i]);?>
		dps[i] = {y: yVal};
	}
	chart.options.data[0].dataPoints = dps;
	chart.render();
};
updateChart();
 
setInterval(function () { updateChart() }, 10000);
 
}
</script>
</head>
<body>
<div id="chartContainer" style="height: 370px; width: 100%;"></div>
<script type="text/javascript" src="https://canvasjs.com/assets/script/canvasjs.min.js"></script>
</body>
</html>
