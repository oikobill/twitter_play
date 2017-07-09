var chart

function fml(){
    if (chart.series.length === 1) {
            data = new Array(20)
        for (i = 0; i < 20; i++) {
          data[i] = [(new Date()).getTime(), 0]
        }
        chart.addSeries({
                name: 'Random Data 2',
            data: data
        });
    }
};

$(document).ready(function () {
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
                        }, 1000);
                    }
                }
            },
           title: {
                text: 'Live random data'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Value'
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
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: true
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'Random data',
                data: (function () {
                    // generate an array of random data
                    var data = [],
                        time = (new Date()).getTime(),
                        i;

                    for (i = -19; i <= 0; i += 1) {
                        data.push({
                            x: time + i * 1000,
                            y: 0
                        });
                    }
                    return data;
                }())
            }]
        });
        // the button handler
        function fml(){
            console.log('fml')
            if (chart.series.length === 1) {
                    data = new Array(20)
                for (i = 0; i < 20; i++) {
                  data[i] = [(new Date()).getTime(), 0]
                }
                chart.addSeries({
                        name: 'Random Data 2',
                    data: data
                });
            }
        };
    });


