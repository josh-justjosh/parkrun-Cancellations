---
layout: page
permalink: /graphs/uk
title: 'UK Graphs'
date: 2021-12-31
---

{% for stuff in site.data.parkrun.raw.time %}
{% assign last_modified_at = stuff.time %}
{% endfor %}

{% if time contains "00:00" %}
  <p class="author_title" id="lastupdated" datetime="{{ last_modified_at | date_to_xmlschema }}">Data Last Refreshed: {{ last_modified_at | date: "%A, %e&nbsp;%B&nbsp;%Y" }}</p>
{% else %}
  <p class="author_title" id="lastupdated" datetime="{{ last_modified_at | date_to_xmlschema }}">Data Last Refreshed: {{ last_modified_at | date: "%R" }} UTC {{ last_modified_at | date: "%A, %e&nbsp;%B&nbsp;%Y" }}</p>
{% endif %}
<script>
    let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZoneName: 'short', hour:'2-digit', minute:'2-digit'};
    var last_modified_at = new Date("{{ last_modified_at }}").getTime();
    var lm_date = new Date(last_modified_at)
    var out = lm_date.toLocaleString('default', options);
    document.getElementById("lastupdated").innerHTML = 'Data Last Refreshed: ' + out
</script>

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
    <div id='headChart'>
        <canvas id="ukChart"></canvas>
    </div>
    <div>
        <h2>5k Events</h2>
        <canvas id="5KChart"></canvas>
    </div>
    <div>
        <h2>junior Events</h2>
        <canvas id="juniorChart"></canvas>
    </div>
    <div>
        <h2>England</h2>
        <canvas id="engChart"></canvas>
    </div>
    <div>
        <h2>Northern Ireland</h2>
        <canvas id="niChart"></canvas>
    </div>
    <div>
        <h2>Scotland</h2>
        <canvas id="scoChart"></canvas>
    </div>
    <div>
        <h2>Wales</h2>
        <canvas id="walChart"></canvas>
    </div>
</div>
<script>
const chartoptions = {
    scales: {
        x: {
            type: 'time',
            title: {
                text: 'Time (UTC)',
                display: true
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
const ukdata = {{ site.data.parkrun.history.unitedkingdom | jsonify }}
const ukconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: ukdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: ukdata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: ukdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: ukdata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var ukChart = new Chart(
    document.getElementById('ukChart'),
    ukconfig
);
const mainconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: ukdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: ukdata,
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
            data: ukdata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: ukdata,
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
const engdata = {{ site.data.parkrun.history.uk.england | jsonify }}
const engconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: engdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: engdata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: engdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: engdata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var engChart = new Chart(
    document.getElementById('engChart'),
    engconfig
);
const nidata = {{ site.data.parkrun.history.uk.ni | jsonify }}
const niconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: nidata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: nidata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: nidata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: nidata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var niChart = new Chart(
    document.getElementById('niChart'),
    niconfig
);
const scodata = {{ site.data.parkrun.history.uk.scotland | jsonify }}
const scoconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: scodata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: scodata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: scodata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: scodata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var scoChart = new Chart(
    document.getElementById('scoChart'),
    scoconfig
);
const waldata = {{ site.data.parkrun.history.uk.wales | jsonify }}
const walconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: waldata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: waldata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: waldata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: waldata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var walChart = new Chart(
    document.getElementById('walChart'),
    walconfig
);
</script>
