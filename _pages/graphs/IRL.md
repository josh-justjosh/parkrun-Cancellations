---
layout: page
permalink: /graphs/irl
title: 'Ireland Graphs'
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.5.1/chart.js" integrity="sha512-b3xr4frvDIeyC3gqR1/iOi6T+m3pLlQyXNuvn5FiRrrKiMUJK3du2QqZbCywH6JxS5EOfW0DY0M6WwdXFbCBLQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>

<style>
    .grid {
            display: grid;
            text-align: center;
            grid-gap: 1rem;
            grid-auto-flow: dense
        }
    #countrytable {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    #headChart {
        grid-column: span 2
    }
    @media (max-width: 670px) {
        #countrytable {
            grid-template-columns: repeat(1, minmax(0, 1fr));
        }
        #headChart {
            grid-column: span 1
        }
    }
    h2 {
        margin: 0
    }
</style>

<div class="grid" id="countrytable">
    <div id="headChart">
        <canvas id="irlChart"></canvas>
    </div>
    <div>
        <h2>5k Events</h2>
        <canvas id="5KChart"></canvas>
    </div>
    <div>
        <h2>junior Events</h2>
        <canvas id="juniorChart"></canvas>
    </div>
</div>
<script>
const chartoptions = {
    scales: {
        x: {
            type: 'time',
            title: {
                text: 'Time (UTC)',
                display: false
            },
            time: {
                minUnit: 'hour',
                displayFormats: {
                    hour: 'h aaa',
                    day: 'eee'
                }
            },
            ticks: {
                major: {
                    enabled: true,
                },
            }
        },
        y: {
            beginAtZero: true,
            ticks: {
                precision: 0
            }
        }
    },
    aspectRatio: 1.5,
    spanGaps: true,
}
const irldata = {{ site.data.history.ireland | jsonify }}
const irlconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: irldata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: irldata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: irldata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: irldata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var irlChart = new Chart(
    document.getElementById('irlChart'),
    irlconfig
);
const mainconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: irldata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: irldata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var mainChart = new Chart(
    document.getElementById('5KChart'),
    mainconfig
);
const juniorconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: irldata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: irldata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var juniorChart = new Chart(
    document.getElementById('juniorChart'),
    juniorconfig
);
</script>
