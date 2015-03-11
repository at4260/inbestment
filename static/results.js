account = Object.keys(results);
	value = account.map(function(key){
		return results[key];
	});
max_account = Object.keys(max_results);
	max_value = max_account.map(function(key){
		return max_results[key];
	});

Highcharts.setOptions({
	lang: {
		thousandsSep: ","
	},
	colors: ['#7cb5ec', '#434348', '#ACA88C']
});

$(function () {
    $('.checkingaccount').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: 'Checking<br>Account',
            align: 'center',
            verticalAlign: 'middle',
            y: 50
        },
        credits: {
            enabled: false
        },
        tooltip: {
            pointFormat: '{series.name}: <b>${point.y:,.2f}</b>'
        },
        plotOptions: {
            pie: {
                dataLabels: {
                    enabled: true,
                    distance: -50,
                    style: {
                        fontWeight: 'bold',
                        color: 'white',
                        textShadow: '0px 1px 2px black'
                    }
                },
                startAngle: -90,
                endAngle: 90,
                center: ['50%', '75%']
            }
        },
        series: [{
            type: 'pie',
            name: 'Value',
            innerSize: '50%',
            data: [
                ['Amount Funded', results["checking"]],
                ['Amount Needed', max_results["checking"] - results["checking"]],
            ]
        }]
    });
});

$(function () {
    $('.savingsaccount').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: 'Savings<br>Account',
            align: 'center',
            verticalAlign: 'middle',
            y: 50
        },
        credits: {
            enabled: false
        },
        tooltip: {
            pointFormat: '{series.name}: <b>${point.y:,.2f}</b>'
        },
        plotOptions: {
            pie: {
                dataLabels: {
                    enabled: true,
                    distance: -50,
                    style: {
                        fontWeight: 'bold',
                        color: 'white',
                        textShadow: '0px 1px 2px black'
                    }
                },
                startAngle: -90,
                endAngle: 90,
                center: ['50%', '75%']
            }
        },
        series: [{
            type: 'pie',
            name: 'Value',
            innerSize: '50%',
            data: [
                ['Amount Funded', results["savings"]],
                ['Amount Needed', max_results["savings"] - results["savings"]],
            ]
        }]
    });
});

if (max_results["match"] !== 0) {
	$(function () {
		$('.matchaccount').highcharts({
			chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: 0,
	            plotShadow: false
	        },
	        credits: {
	            enabled: false
	        },	        
	        tooltip: {
	            pointFormat: '{series.name}: <b>${point.y:,.2f}</b>'
	        },
	        plotOptions: {
	            pie: {
	                dataLabels: {
	                    enabled: true,
	                    distance: -50,
	                    style: {
	                        fontWeight: 'bold',
	                        color: 'white',
	                        textShadow: '0px 1px 2px black'
	                    }
	                },
	                startAngle: -90,
	                endAngle: 90,
	                center: ['50%', '75%']
	            }
	        },
	        title: {
	            text: '401K Match',
	            align: 'center',
	            verticalAlign: 'middle',
	            y: 50
	        },	        
	        series: [{
	            type: 'pie',
	            name: 'Value',
	            innerSize: '50%',
	            data: [
	                ['Amount Funded', results["match"]],
	                ['Amount Needed', max_results["match"] - results["match"]],
	            ]
	        }],
    	});
	});
} else {
	$(function () {
		$('.matchaccount').highcharts({
			chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: 0,
	            plotShadow: false
	        },
	        credits: {
	            enabled: false
	        },	        
	        tooltip: {
	        	enabled: false,
	            pointFormat: '{series.name}: <b>${point.y:,.2f}</b>'
	        },
	        plotOptions: {
	            pie: {
	                dataLabels: {
	                    enabled: true,
	                    distance: -50,
	                    style: {
	                        fontWeight: 'bold',
	                        color: 'white',
	                        textShadow: '0px 1px 2px black'
	                    }
	                },
	                startAngle: -90,
	                endAngle: 90,
	                center: ['50%', '75%']
	            }
	        },
	        title: {
	            text: '401K Match',
	            align: 'center',
	            verticalAlign: 'middle',
	            y: 50
	        },	        
	        series: [{
	            type: 'pie',
	            name: 'Value',
	            innerSize: '50%',
	            // Including 4 empty arrays in order to get the color 
	            // that I want from the Highcharts Color list.
	            data: [
	            	['', 0],
	            	['', 0],
	                ['Not Applicable', 100],
	            ]
	        }],
    	});
	});
}

$(function () {
    $('.iraaccount').highcharts({
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: 0,
            plotShadow: false
        },
        title: {
            text: 'IRA',
            align: 'center',
            verticalAlign: 'middle',
            y: 50
        },
        credits: {
            enabled: false
        },
        tooltip: {
            pointFormat: '{series.name}: <b>${point.y:,.2f}</b>'
        },
        plotOptions: {
            pie: {
                dataLabels: {
                    enabled: true,
                    distance: -50,
                    style: {
                        fontWeight: 'bold',
                        color: 'white',
                        textShadow: '0px 1px 2px black'
                    }
                },
                startAngle: -90,
                endAngle: 90,
                center: ['50%', '75%']
            }
        },
        series: [{
            type: 'pie',
            name: 'Value',
            innerSize: '50%',
            data: [
                ['Amount Funded', results["ira"]],
                ['Amount Needed', max_results["ira"] - results["ira"]],
            ]
        }]
    });
});

if (max_results["ret401k"] !== 0) {	
	$(function () {
	    $('.ret401kaccount').highcharts({
	        chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: 0,
	            plotShadow: false
	        },
	        title: {
	            text: '401K<br>Account',
	            align: 'center',
	            verticalAlign: 'middle',
	            y: 50
	        },
	        credits: {
	            enabled: false
	        },
	        tooltip: {
	            pointFormat: '{series.name}: <b>${point.y:,.2f}</b>'
	        },
	        plotOptions: {
	            pie: {
	                dataLabels: {
	                    enabled: true,
	                    distance: -50,
	                    style: {
	                        fontWeight: 'bold',
	                        color: 'white',
	                        textShadow: '0px 1px 2px black'
	                    }
	                },
	                startAngle: -90,
	                endAngle: 90,
	                center: ['50%', '75%']
	            }
	        },
	        series: [{
	            type: 'pie',
	            name: 'Value',
	            innerSize: '50%',
	            data: [
	                ['Amount Funded', results["ret401k"]],
	                ['Amount Needed', max_results["ret401k"] - results["ret401k"]],
	            ]
	        }]
	    });
	});
} else {
	$(function () {
	    $('.ret401kaccount').highcharts({
	        chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: 0,
	            plotShadow: false
	        },
	        title: {
	            text: '401K<br>Account',
	            align: 'center',
	            verticalAlign: 'middle',
	            y: 50
	        },
	        credits: {
	            enabled: false
	        },
	        tooltip: {
	        	enabled: false,
	            pointFormat: '{series.name}: <b>${point.y:,.2f}</b>'
	        },
	        plotOptions: {
	            pie: {
	                dataLabels: {
	                    enabled: true,
	                    distance: -50,
	                    style: {
	                        fontWeight: 'bold',
	                        color: 'white',
	                        textShadow: '0px 1px 2px black'
	                    }
	                },
	                startAngle: -90,
	                endAngle: 90,
	                center: ['50%', '75%']
	            }
	        },
	        series: [{
	            type: 'pie',
	            name: 'Value',
	            innerSize: '50%',
	            data: [
	            	['', 0],
	            	['', 0],
	            	['Not Applicable', 100],
            	]
	        }]
	    });
	});
}

if (results["investment"] !== 0) {	
	$(function () {
	    $('.investmentaccount').highcharts({
	        chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: 0,
	            plotShadow: false
	        },
	        title: {
	            text: 'Brokerage<br>Account',
	            align: 'center',
	            verticalAlign: 'middle',
	            y: 50
	        },
	        credits: {
	            enabled: false
	        },
	        tooltip: {
	            pointFormat: '{series.name}: <b>${point.y:,.2f}</b>'
	        },
	        plotOptions: {
	            pie: {
	                dataLabels: {
	                    enabled: true,
	                    distance: -50,
	                    style: {
	                        fontWeight: 'bold',
	                        color: 'white',
	                        textShadow: '0px 1px 2px black'
	                    }
	                },
	                startAngle: -90,
	                endAngle: 90,
	                center: ['50%', '75%']
	            }
	        },
	        series: [{
	            type: 'pie',
	            name: 'Value',
	            innerSize: '50%',
	            data: [
	                ['Amount Funded', results["investment"]]
	            ]
	        }]
	    });
	});
} else {
	$(function () {
	    $('.investmentaccount').highcharts({
	        chart: {
	            plotBackgroundColor: null,
	            plotBorderWidth: 0,
	            plotShadow: false
	        },
	        title: {
	            text: 'Brokerage<br>Account',
	            align: 'center',
	            verticalAlign: 'middle',
	            y: 50
	        },
	        credits: {
	            enabled: false
	        },
	        tooltip: {
	        	enabled: false,
	            pointFormat: '{series.name}: <b>${point.y:,.2f}</b>'
	        },
	        plotOptions: {
	            pie: {
	                dataLabels: {
	                    enabled: true,
	                    distance: -50,
	                    style: {
	                        fontWeight: 'bold',
	                        color: 'white',
	                        textShadow: '0px 1px 2px black'
	                    }
	                },
	                startAngle: -90,
	                endAngle: 90,
	                center: ['50%', '75%']
	            }
	        },
	        series: [{
	            type: 'pie',
	            name: 'Value',
	            innerSize: '50%',
	            data: [
	            	['', 0],
	            	['', 0],
	                ['Not Applicable', 100],
	            ]
	        }]
	    });
	});
}