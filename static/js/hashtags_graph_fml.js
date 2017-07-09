var chart
var frequency = 5
var title = ('Hashtag References per '.concat(frequency.toString())).concat(' Seconds')
var repeats = 20
var max_hashtags = 3

// append plot for new hashtag
function add_hashtag(){
    if (chart.series.length < max_hashtags) {
        data = new Array(repeats)
        time = (new Date()).getTime() - (repeats - 1) * 1000
        for(i = 0; i < repeats; i++) {
            data[i] = [time + i * 1000, 0]
        }
        var last_hashtag = document.getElementById('hashtag_input').value
        chart.addSeries({
            name: last_hashtag,
            data: data
        });
    }
};

$(document).ready(function () {
        // enable local time
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });

        // set up graph chart
        chart = new Highcharts.Chart({
            chart: {
                renderTo: 'container_hashtags_graph',
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function () {
                        // set up the updating of the chart each second
                        var series = this.series;
                        setInterval(function () {
                                for (i = 0; i < series.length; i++) {
                                    var x = (new Date()).getTime(), // current time
                                        y = Math.random();
                                    series[i].addPoint([x, y], true, true);
                            }
                        }, 5000);
                    }
                }
            },
           title: {
                text: title
            },
            xAxis: {
                text: 'Time',
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Hashtag Count'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }],
                min: 0
            },
            tooltip: {
                formatter: function () {
                    return '<b>' + this.series.name + ': </b>' + Highcharts.numberFormat(this.y, 2);
                }
            },
            exporting: {
                enabled: false
            },
            series: []
        });
    });


