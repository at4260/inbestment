// CREATES PERFORMANCE TOGGLE
$("#line_total").click(function() {
    $("#total_performance").show();
    $("#all_performance").hide();   
    $("#allocation").hide();
});
$("#line_individual").click(function() {
    $("#total_performance").hide();
    $("#all_performance").show();
    $("#allocation").hide();
});
$("#pie").click(function() {
    $("#total_performance").hide();
    $("#all_performance").hide();
    $("#allocation").show();
});

// CREATES PERFORMANCE LINE GRAPHS
$(function () { 
    $('#total_performance').highcharts({
        chart: {
            type: 'area'
        },
        title: {
            text: 'Total Portfolio Performance'
        },
        xAxis: {
            categories: dates,
            tickInterval: 125
        },
        yAxis: {
            title: {
                text: 'Percent Change'
            }
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.y:,.4f}</b>'
        },
        credits: {
            enabled: false
        },
        series: [{
            name: 'Total',
            data: total_performance
        }]
    });
});

$(function () { 
    Highcharts.setOptions({
        colors: ['#7cb5ec', '#434348', '#576E7F', '#88B0BF', '#B2B2B2']
    });
    $('#all_performance').highcharts({
        chart: {
            type: 'area',
        },
        title: {
            text: 'Individual Fund Performance'
        },
        xAxis: {
            categories: dates,
            tickInterval: 125
        },
        yAxis: {
            title: {
                text: 'Percent Change'
            }
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.y:,.4f}</b>'
        },
        credits: {
            enabled: false
        },
        series: [{
                name: prof_ticker_data[1][0],
            data: ticker_query_1
        }, {
            name: prof_ticker_data[1][1],
            data: ticker_query_2
        }, {
            name: prof_ticker_data[1][2],
            data: ticker_query_3
        }, {
            name: prof_ticker_data[1][3],
            data: ticker_query_4
        }, {
            name: prof_ticker_data[1][4],
            data: ticker_query_5
        }]
    });
});

// CREATES ALLOCATION PIE CHART
chart_categories = Object.keys(chart_ticker_data);
chart_stock_data = chart_ticker_data["Stocks"];
chart_stock_funds = Object.keys(chart_stock_data);
chart_stock_weights = chart_stock_funds.map(function(key){
	return chart_stock_data[key];
});
// Creates inner circle of total stock allocation
var chart_stock_sum = 0;
var len = chart_stock_weights.length
for(var i = 0; i < len; i++){
    chart_stock_sum = chart_stock_sum + chart_stock_weights[i]
}
chart_bond_data = chart_ticker_data["Bonds"];
chart_bond_funds = Object.keys(chart_bond_data);
chart_bond_weights = chart_bond_funds.map(function(key){
	return chart_bond_data[key];
});
// Creates inner circle of total bond allocation
var chart_bond_sum = 0;
var len = chart_bond_weights.length
for(var i = 0; i < len; i++){
    chart_bond_sum = chart_bond_sum + chart_bond_weights[i]
}
$(function () {
    var colors = Highcharts.getOptions().colors,
        categories = chart_categories,
        data = [{
            y: chart_stock_sum,
            color: colors[0],
            drilldown: {
                name: "Stocks Funds",
                categories: chart_stock_funds,
                data: chart_stock_weights,
                color: colors[0]
            }
        }, {
            y: chart_bond_sum,
            color: colors[1],
            drilldown: {
                name: "Bonds Funds",
                categories: chart_bond_funds,
                data: chart_bond_weights,
                color: colors[1]
            }
        }],
        browserData = [],
        versionsData = [],
        i,
        j,
        dataLen = data.length,
        drillDataLen,
        brightness;
    // Build the data arrays
    for (i = 0; i < dataLen; i += 1) {
        // add browser data
        browserData.push({
            name: categories[i],
            y: data[i].y,
            color: data[i].color
        });
        // add version data
        drillDataLen = data[i].drilldown.data.length;
        for (j = 0; j < drillDataLen; j += 1) {
            brightness = 0.2 - (j / drillDataLen) / 5;
            versionsData.push({
                name: data[i].drilldown.categories[j],
                y: data[i].drilldown.data[j],
                color: Highcharts.Color(data[i].color).brighten(
                    brightness).get()
            });
        }
    }
    // Create the chart
    $('#allocation').highcharts({
        chart: {
            type: 'pie'
        },
        title: {
            text: 'Recommended Allocation'
        },
        yAxis: {
            title: {
                text: 'Total percent allocation'
            }
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            pie: {
                shadow: false,
                center: ['50%', '50%']
            }
        },
        tooltip: {
            valueSuffix: '%'
        },
        series: [{
            name: 'Category',
            data: browserData,
            size: '60%',
            dataLabels: {
                formatter: function () {
                    return this.y > 5 ? this.point.name : null;
                },
                color: 'white',
                distance: -50
            }
        }, {
            name: 'Fund',
            data: versionsData,
            size: '80%',
            innerSize: '60%',
            dataLabels: {
                formatter: function () {
                    // display only if larger than 1
                    return this.y > 1 ? '<b>' + this.point.name + 
                    ':</b> ' + this.y + '%'  : null;
                },
                distance: 10
            }
        }]
    });
});
