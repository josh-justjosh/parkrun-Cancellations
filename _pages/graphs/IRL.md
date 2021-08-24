---
layout: page
permalink: /graphs/irl
title: 'Ireland Graphs'
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
    @media (max-width: 670px) {
        #countrytable {
        grid-template-columns: repeat(1, minmax(0, 1fr));
    }
    }
</style>
<div>
    <canvas id="irlChart"></canvas>
</div>
<div class="grid" id="countrytable">
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
const irldata = {{ site.data.parkrun.history.ireland | jsonify }}
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
    options: {
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
        aspectRatio: 1.75,
    }
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
    options: {
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
        aspectRatio: 1.75,
    }
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
    options: {
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
        aspectRatio: 1.75,
    }
};
var juniorChart = new Chart(
    document.getElementById('juniorChart'),
    juniorconfig
);
</script>
