window.onload = function () {

var chart = new CanvasJS.Chart("chartContainer", {
	exportEnabled: false,
	animationEnabled: true,
	title:{
		text: ""
	},
	legend:{
		cursor: "pointer",
		itemclick: explodePie
	},
	data: [{
		type: "pie",
		showInLegend: true,
		toolTipContent: "{name}: <strong>{y}%</strong>",
		indexLabel: "{name} - {y}%",
		dataPoints: [
			{ y: 26, name: "Engineering", exploded: true },
			{ y: 20, name: "Technology" },
			{ y: 5, name: "Maintenance" },
			{ y: 3, name: "Chemical" },
			{ y: 7, name: "Petroleum " },
			{ y: 17, name: "Gas" },
			{ y: 22, name: "Assistance"}
		]
	}]
});
chart.render();
}

function explodePie (e) {
	if(typeof (e.dataSeries.dataPoints[e.dataPointIndex].exploded) === "undefined" || !e.dataSeries.dataPoints[e.dataPointIndex].exploded) {
		e.dataSeries.dataPoints[e.dataPointIndex].exploded = true;
	} else {
		e.dataSeries.dataPoints[e.dataPointIndex].exploded = false;
	}
	e.chart.render();

}