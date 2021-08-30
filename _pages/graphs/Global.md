---
layout: page
permalink: /graphs/global
title: 'Global Events'
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
    <div id="headChart">
        <canvas id="countriesChart"></canvas>
    </div>
    <div>
        <h2><a href="/graphs/aus">Australia</a></h2>
        <canvas id="australiaChart"></canvas>
    </div>
    <div>
        <h2>Austria</h2>
        <canvas id="austriaChart"></canvas>
    </div>
    <div>
        <h2>Canada</h2>
        <canvas id="canadaChart"></canvas>
    </div>
    <div>
        <h2>Denmark</h2>
        <canvas id="denmarkChart"></canvas>
    </div>
    <div>
        <h2>Eswatini</h2>
        <canvas id="eswatiniChart"></canvas>
    </div>
    <div>
        <h2>Finalnd</h2>
        <canvas id="finlandChart"></canvas>
    </div>
    <div>
        <h2>France</h2>
        <canvas id="franceChart"></canvas>
    </div>
    <div>
        <h2>Germany</h2>
        <canvas id="germanyChart"></canvas>
    </div>
    <div>
        <h2><a href="/graphs/irl">Ireland</a></h2>
        <canvas id="irelandChart"></canvas>
    </div>
    <div>
        <h2>Italy</h2>
        <canvas id="italyChart"></canvas>
    </div>
    <div>
        <h2>Japan</h2>
        <canvas id="japanChart"></canvas>
    </div>
    <div>
        <h2>Malaysia</h2>
        <canvas id="malaysiaChart"></canvas>
    </div>
    <div>
        <h2>Namibia</h2>
        <canvas id="namibiaChart"></canvas>
    </div>
    <div>
        <h2>Netherlands</h2>
        <canvas id="netherlandsChart"></canvas>
    </div>
    <div id='NZ'>
        <h2>New Zealand</h2>
        <canvas id="newzealandChart"></canvas>
    </div>
    <div>
        <h2>Norway</h2>
        <canvas id="norwayChart"></canvas>
    </div>
    <div>
        <h2>Poland</h2>
        <canvas id="polandChart"></canvas>
    </div>
    <div>
        <h2>Russia</h2>
        <canvas id="russiaChart"></canvas>
    </div>
    <div>
        <h2>Singapore</h2>
        <canvas id="singaporeChart"></canvas>
    </div>
    <div>
        <h2>South Africa</h2>
        <canvas id="southafricaChart"></canvas>
    </div>
    <div>
        <h2>Sweden</h2>
        <canvas id="swedenChart"></canvas>
    </div>
    <div>
        <h2><a href="/graphs/uk">United Kingdom</a></h2>
        <canvas id="ukChart"></canvas>
    </div>
    <div>
        <h2>USA</h2>
        <canvas id="usaChart"></canvas>
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
const countriesdata = {{ site.data.parkrun.history.global | jsonify }}
const countriesconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: countriesdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: countriesdata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: countriesdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: countriesdata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var countriesChart = new Chart(
    document.getElementById('countriesChart'),
    countriesconfig
);
const australiadata = {{ site.data.parkrun.history.australia | jsonify }}
const australiaconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: australiadata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: australiadata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: australiadata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: australiadata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var australiaChart = new Chart(
    document.getElementById('australiaChart'),
    australiaconfig
);
const austriadata = {{ site.data.parkrun.history.austria | jsonify }}
const austriaconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: austriadata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        //},{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: austriadata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: austriadata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //   label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: austriadata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var austriaChart = new Chart(
    document.getElementById('austriaChart'),
    austriaconfig
);
const canadadata = {{ site.data.parkrun.history.canada | jsonify }}
const canadaconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: canadadata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: canadadata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: canadadata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: canadadata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var canadaChart = new Chart(
    document.getElementById('canadaChart'),
    canadaconfig
);
const denmarkdata = {{ site.data.parkrun.history.denmark | jsonify }}
const denmarkconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: denmarkdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: denmarkdata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: denmarkdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: denmarkdata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var denmarkChart = new Chart(
    document.getElementById('denmarkChart'),
    denmarkconfig
);
const eswatinidata = {{ site.data.parkrun.history.eswatini | jsonify }}
const eswatiniconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: eswatinidata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: eswatinidata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: eswatinidata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: eswatinidata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var eswatiniChart = new Chart(
    document.getElementById('eswatiniChart'),
    eswatiniconfig
);
const finlanddata = {{ site.data.parkrun.history.finland | jsonify }}
const finlandconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: finlanddata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: finlanddata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: finlanddata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: finlanddata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var finlandChart = new Chart(
    document.getElementById('finlandChart'),
    finlandconfig
);
const francedata = {{ site.data.parkrun.history.france | jsonify }}
const franceconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: francedata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: francedata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: francedata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: francedata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var franceChart = new Chart(
    document.getElementById('franceChart'),
    franceconfig
);
const germanydata = {{ site.data.parkrun.history.germany | jsonify }}
const germanyconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: germanydata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: germanydata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: germanydata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: germanydata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var germanyChart = new Chart(
    document.getElementById('germanyChart'),
    germanyconfig
);
const irelanddata = {{ site.data.parkrun.history.ireland | jsonify }}
const irelandconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: irelanddata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: irelanddata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: irelanddata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: irelanddata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var irelandChart = new Chart(
    document.getElementById('irelandChart'),
    irelandconfig
);
const italydata = {{ site.data.parkrun.history.italy | jsonify }}
const italyconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: italydata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: italydata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: italydata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: italydata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var italyChart = new Chart(
    document.getElementById('italyChart'),
    italyconfig
);
const japandata = {{ site.data.parkrun.history.japan | jsonify }}
const japanconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: japandata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: japandata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: japandata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: japandata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var japanChart = new Chart(
    document.getElementById('japanChart'),
    japanconfig
);
const malaysiadata = {{ site.data.parkrun.history.malaysia | jsonify }}
const malaysiaconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: malaysiadata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: malaysiadata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: malaysiadata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: malaysiadata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var malaysiaChart = new Chart(
    document.getElementById('malaysiaChart'),
    malaysiaconfig
);
const namibiadata = {{ site.data.parkrun.history.namibia | jsonify }}
const namibiaconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: namibiadata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: namibiadata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: namibiadata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: namibiadata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var namibiaChart = new Chart(
    document.getElementById('namibiaChart'),
    namibiaconfig
);
const netherlandsdata = {{ site.data.parkrun.history.netherlands | jsonify }}
const netherlandsconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: netherlandsdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: netherlandsdata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: netherlandsdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: netherlandsdata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var netherlandsChart = new Chart(
    document.getElementById('netherlandsChart'),
    netherlandsconfig
);
const newzealanddata = {{ site.data.parkrun.history.newzealand | jsonify }}
const newzealandconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: newzealanddata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: newzealanddata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: newzealanddata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: newzealanddata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var newzealandChart = new Chart(
    document.getElementById('newzealandChart'),
    newzealandconfig
);
const norwaydata = {{ site.data.parkrun.history.norway | jsonify }}
const norwayconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: norwaydata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: norwaydata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: norwaydata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: norwaydata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var norwayChart = new Chart(
    document.getElementById('norwayChart'),
    norwayconfig
);
const polanddata = {{ site.data.parkrun.history.poland | jsonify }}
const polandconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: polanddata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: polanddata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: polanddata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: polanddata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var polandChart = new Chart(
    document.getElementById('polandChart'),
    polandconfig
);
const russiadata = {{ site.data.parkrun.history.russia | jsonify }}
const russiaconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: russiadata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: russiadata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: russiadata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: russiadata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var russiaChart = new Chart(
    document.getElementById('russiaChart'),
    russiaconfig
);
const singaporedata = {{ site.data.parkrun.history.singapore | jsonify }}
const singaporeconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: singaporedata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: singaporedata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: singaporedata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: singaporedata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var singaporeChart = new Chart(
    document.getElementById('singaporeChart'),
    singaporeconfig
);
const southafricadata = {{ site.data.parkrun.history.southafrica | jsonify }}
const southafricaconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: southafricadata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: southafricadata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: southafricadata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: southafricadata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var southafricaChart = new Chart(
    document.getElementById('southafricaChart'),
    southafricaconfig
);
const swedendata = {{ site.data.parkrun.history.sweden | jsonify }}
const swedenconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: swedendata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: swedendata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: swedendata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: swedendata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var swedenChart = new Chart(
    document.getElementById('swedenChart'),
    swedenconfig
);
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
const usadata = {{ site.data.parkrun.history.usa | jsonify }}
const usaconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: usadata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: usadata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: usadata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: usadata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var usaChart = new Chart(
    document.getElementById('usaChart'),
    usaconfig
);
</script>
