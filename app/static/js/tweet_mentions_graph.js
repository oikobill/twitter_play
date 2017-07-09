var chart
var frequency = 30
var title = ('Tweet Mentions per '.concat(frequency.toString())).concat(' Seconds')
var repeats = 20
var max_terms = 1

// append plot for new hashtag
function add_mention(){
    if (chart.series.length < max_terms) {
        // generate dummy starting points with y=0
        data = new Array(repeats)
        time = (new Date()).getTime() - (repeats - 1) * 1000
        for(i = 0; i < repeats; i++) {
            data[i] = [time + i * 1000, 0]
        }

        // setup chart and initiate server tweet search
        var last_term = document.getElementById('term_input').value
        start_search_mentions(last_term)
        chart.addSeries({
            name: last_term,
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
                renderTo: 'container_mentions_graph',
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function () {
                        // set up the updating of the chart <frequency> seconds
                        var series = this.series;
                        setInterval(function () {
                                for (i = 0; i < series.length; i++) {
                                    var x = (new Date()).getTime(), // current time
                                        y = get_tweet_counts(frequency); //  //Math.random(); //
                                    series[i].addPoint([x, y], true, true);
                            }
                        }, frequency * 1000);
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
                    text: 'Tweet Mentions'
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
                    return '<b>' + this.series.name + ': </b>' + Highcharts.numberFormat(this.y, 2) + ' tweets';
                }
            },
            exporting: {
                enabled: false
            },
            series: []
        });
    });


