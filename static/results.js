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
	colors: ['#7cb5ec', '#434348', '#737373']
});

$(function () {
    $('.checkingaccount').highcharts({
        chart: {
            plotBackgroundColor: '#eeeeee',
            plotBorderWidth: 0,
            plotShadow: false,
            spacing: [-50, -50, -50, -50]
        },
        title: {
            text: 'Checking',
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
                    distance: -40,
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
                ['Target Remaining', max_results["checking"] 
                - results["checking"]],
            ]
        }]
    });
});

$(function () {
    $('.savingsaccount').highcharts({
        chart: {
            plotBackgroundColor: '#eeeeee',
        	plotBorderWidth: 0,
        	plotShadow: false,
        	spacing: [-50, -50, -50, -50]
        },
        title: {
            text: 'Savings',
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
                    distance: -40,
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
                ['Target Remaining', max_results["savings"] 
                - results["savings"]],
            ]
        }]
    });
});

if (max_results["match"] !== 0) {
	$(function () {
		$('.matchaccount').highcharts({
			chart: {
	            plotBackgroundColor: '#eeeeee',
            	plotBorderWidth: 0,
            	plotShadow: false,
            	spacing: [-50, -50, -50, -50]
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
	                    distance: -40,
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
	                ['Target Remaining', max_results["match"] 
	                - results["match"]],
	            ]
	        }],
    	});
	});
} else {
	$(function () {
		$('.matchaccount').highcharts({
			chart: {
	            plotBackgroundColor: '#eeeeee',
            	plotBorderWidth: 0,
            	plotShadow: false,
            	spacing: [-50, -50, -50, -50]
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
	                    distance: -40,
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
	            plotBackgroundColor: '#eeeeee',
            	plotBorderWidth: 0,
            	plotShadow: false,
            	spacing: [-50, -50, -50, -50]
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
                    distance: -40,
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
                ['Target Remaining', max_results["ira"] - results["ira"]],
            ]
        }]
    });
});

if (max_results["ret401k"] !== 0) {	
	$(function () {
	    $('.ret401kaccount').highcharts({
	        chart: {
	            plotBackgroundColor: '#eeeeee',
            	plotBorderWidth: 0,
            	plotShadow: false,
            	spacing: [-50, -50, -50, -50]
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
	                    distance: -40,
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
	                ['Target Remaining', max_results["ret401k"] 
	                - results["ret401k"]],
	            ]
	        }]
	    });
	});
} else {
	$(function () {
	    $('.ret401kaccount').highcharts({
	        chart: {
	            plotBackgroundColor: '#eeeeee',
            	plotBorderWidth: 0,
            	plotShadow: false,
            	spacing: [-50, -50, -50, -50]
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
	                    distance: -40,
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
	            plotBackgroundColor: '#eeeeee',
            	plotBorderWidth: 0,
            	plotShadow: false,
            	spacing: [-50, -50, -50, -50]
	        },
	        title: {
	            text: 'Brokerage',
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
	                    distance: -40,
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
	            plotBackgroundColor: '#eeeeee',
            	plotBorderWidth: 0,
            	plotShadow: false,
            	spacing: [-50, -50, -50, -50]
	        },
	        title: {
	            text: 'Brokerage',
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
	                    distance: -40,
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
