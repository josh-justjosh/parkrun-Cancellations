---
layout: page
permalink: /graphs/aus
title: 'Australia Graphs'
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
        <canvas id="ausChart"></canvas>
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
        <h2>Australian Capital Territory</h2>
        <canvas id="actChart"></canvas>
    </div>
    <div>
        <h2>New South Wales</h2>
        <canvas id="nswChart"></canvas>
    </div>
    <div>
        <h2>Northern Territory</h2>
        <canvas id="ntChart"></canvas>
    </div>
    <div>
        <h2>Queensland</h2>
        <canvas id="qldChart"></canvas>
    </div>
    <div>
        <h2>South Australia</h2>
        <canvas id="saChart"></canvas>
    </div>
    <div>
        <h2>Tasmania</h2>
        <canvas id="tasChart"></canvas>
    </div>
    <div>
        <h2>Victoria</h2>
        <canvas id="vicChart"></canvas>
    </div>
    <div>
        <h2>Western Australia</h2>
        <canvas id="waChart"></canvas>
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
const ausdata = {{ site.data.history.australia | jsonify }}
const ausconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: ausdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: ausdata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: ausdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: ausdata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var ausChart = new Chart(
    document.getElementById('ausChart'),
    ausconfig
);
const mainconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: ausdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: ausdata,
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
            data: ausdata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: ausdata,
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
const actdata = {{ site.data.history.aus.act | jsonify }}
const actconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: actdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            //label: 'junior parkrunning',
            //backgroundColor: '#0288D1',
            //borderColor: '#0288D1',
            //data: actdata,
            //parsing: {
                //yAxisKey: 'junior parkrunning',
                //xAxisKey: 'time'
            //}
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: actdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
            //label: 'junior Cancellations',
            //backgroundColor: '#1A237E',
            //borderColor: '#1A237E',
            //data: actdata,
            //parsing: {
                //yAxisKey: 'junior Cancellations',
                //xAxisKey: 'time'
            //}
        //}
        ]
    },
    options: chartoptions
};
var actChart = new Chart(
    document.getElementById('actChart'),
    actconfig
);
const nswdata = {{ site.data.history.aus.nsw | jsonify }}
const nswconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: nswdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        //},{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: nswdata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: nswdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: nswdata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var nswChart = new Chart(
    document.getElementById('nswChart'),
    nswconfig
);
const ntdata = {{ site.data.history.aus.nt | jsonify }}
const ntconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: ntdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: ntdata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: ntdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: ntdata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var ntChart = new Chart(
    document.getElementById('ntChart'),
    ntconfig
);
const qlddata = {{ site.data.history.aus.qld | jsonify }}
const qldconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: qlddata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: qlddata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: qlddata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: qlddata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var qldChart = new Chart(
    document.getElementById('qldChart'),
    qldconfig
);
const sadata = {{ site.data.history.aus.sa | jsonify }}
const saconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: sadata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: sadata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: sadata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: sadata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var saChart = new Chart(
    document.getElementById('saChart'),
    saconfig
);
const tasdata = {{ site.data.history.aus.tas | jsonify }}
const tasconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: tasdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        //},{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: tasdata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: tasdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: tasdata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var tasChart = new Chart(
    document.getElementById('tasChart'),
    tasconfig
);
const vicdata = {{ site.data.history.aus.vic | jsonify }}
const vicconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: vicdata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: 'junior parkrunning',
            backgroundColor: '#0288D1',
            borderColor: '#0288D1',
            data: vicdata,
            parsing: {
                yAxisKey: 'junior parkrunning',
                xAxisKey: 'time'
            }
        },{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: vicdata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        },{
            label: 'junior Cancellations',
            backgroundColor: '#1A237E',
            borderColor: '#1A237E',
            data: vicdata,
            parsing: {
                yAxisKey: 'junior Cancellations',
                xAxisKey: 'time'
            }
        }]
    },
    options: chartoptions
};
var vicChart = new Chart(
    document.getElementById('vicChart'),
    vicconfig
);
const wadata = {{ site.data.history.aus.wa | jsonify }}
const waconfig = {
    type: 'line',
    data: {
        datasets:[{
            label: 'parkrunning',
            backgroundColor: '#7CB342',
            borderColor: '#7CB342',
            data: wadata,
            parsing: {
                yAxisKey: 'parkrunning',
                xAxisKey: 'time'
            }
        },{
        //    label: 'junior parkrunning',
        //    backgroundColor: '#0288D1',
        //    borderColor: '#0288D1',
        //    data: wadata,
        //    parsing: {
        //        yAxisKey: 'junior parkrunning',
        //        xAxisKey: 'time'
        //    }
        //},{
            label: '5k Cancellations',
            backgroundColor: '#A52714',
            borderColor: '#A52714',
            data: wadata,
            parsing: {
                yAxisKey: '5k Cancellations',
                xAxisKey: 'time'
            }
        }//,{
        //    label: 'junior Cancellations',
        //    backgroundColor: '#1A237E',
        //    borderColor: '#1A237E',
        //    data: wadata,
        //    parsing: {
        //        yAxisKey: 'junior Cancellations',
        //        xAxisKey: 'time'
        //    }
        //}
        ]
    },
    options: chartoptions
};
var waChart = new Chart(
    document.getElementById('waChart'),
    waconfig
);
</script>
