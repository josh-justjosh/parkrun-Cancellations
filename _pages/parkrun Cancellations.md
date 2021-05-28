---
layout: page
title: parkrun Cancellations
tag: parkrun
date: 2021-05-27
permalink: /parkrun-cancellations/
---

{% for stuff in site.data.raw.time %}
{% assign last_modified_at = stuff.time %}
{% endfor %}

{% assign time = last_modified_at | date: "%R" %}
{% assign tz = last_modified_at | date: "%z" %}
{% if tz == "+0000" %}{% assign tzn = "UTC" %}
{% elsif tz == "+0100" %}{% assign tzn = "UTC+1" %}
{% elsif tz == "-1200" %}{% assign tzn = "UTC-12" %}
{% elsif tz == "-1100" %}{% assign tzn = "UTC-11" %}
{% elsif tz == "-1000" %}{% assign tzn = "UTC-10" %}
{% elsif tz == "-0930" %}{% assign tzn = "UTC-09:30" %}
{% elsif tz == "-0900" %}{% assign tzn = "UTC-9" %}
{% elsif tz == "-0800" %}{% assign tzn = "UTC-8" %}
{% elsif tz == "-0700" %}{% assign tzn = "UTC-7" %}
{% elsif tz == "-0600" %}{% assign tzn = "UTC-6" %}
{% elsif tz == "-0500" %}{% assign tzn = "UTC-5" %}
{% elsif tz == "-0400" %}{% assign tzn = "UTC-4" %}
{% elsif tz == "-0330" %}{% assign tzn = "UTC-03:30" %}
{% elsif tz == "-0300" %}{% assign tzn = "UTC-3" %}
{% elsif tz == "-0230" %}{% assign tzn = "UTC-02:30" %}
{% elsif tz == "-0200" %}{% assign tzn = "UTC-2" %}
{% elsif tz == "-0100" %}{% assign tzn = "UTC-1" %}
{% elsif tz == "+0200" %}{% assign tzn = "UTC+2" %}
{% elsif tz == "+0300" %}{% assign tzn = "UTC+3" %}
{% elsif tz == "+0330" %}{% assign tzn = "UTC+03:30" %}
{% elsif tz == "+0400" %}{% assign tzn = "UTC+4" %}
{% elsif tz == "+0430" %}{% assign tzn = "UTC+04:30" %}
{% elsif tz == "+0500" %}{% assign tzn = "UTC+5" %}
{% elsif tz == "+0530" %}{% assign tzn = "UTC+05:30" %}
{% elsif tz == "+0545" %}{% assign tzn = "UTC+05:45" %}
{% elsif tz == "+0600" %}{% assign tzn = "UTC+6" %}
{% elsif tz == "+0630" %}{% assign tzn = "UTC+06:30" %}
{% elsif tz == "+0700" %}{% assign tzn = "UTC+7" %}
{% elsif tz == "+0800" %}{% assign tzn = "UTC+8" %}
{% elsif tz == "+0845" %}{% assign tzn = "UTC+08:45" %}
{% elsif tz == "+0900" %}{% assign tzn = "UTC+9" %}
{% elsif tz == "+0930" %}{% assign tzn = "UTC+09:30" %}
{% elsif tz == "+1000" %}{% assign tzn = "UTC+10" %}
{% elsif tz == "+1030" %}{% assign tzn = "UTC+10:30" %}
{% elsif tz == "+1100" %}{% assign tzn = "UTC+11" %}
{% elsif tz == "+1200" %}{% assign tzn = "UTC+12" %}
{% elsif tz == "+1245" %}{% assign tzn = "UTC+12:45" %}
{% elsif tz == "+1300" %}{% assign tzn = "UTC+13" %}
{% elsif tz == "+1345" %}{% assign tzn = "UTC+13:45" %}
{% elsif tz == "+1400" %}{% assign tzn = "UTC+14" %}
{% else %}{% assign tzn = "UTC" | append: tz %}
{% endif %}
{% if time contains "00:00" %}
  <p class="author_title" datetime="{{ last_modified_at | date_to_xmlschema }}">Last Updated: {{ last_modified_at | date: "%A, %e&nbsp;%B&nbsp;%Y" }}</p>
{% else %}
  <p class="author_title" datetime="{{ last_modified_at | date_to_xmlschema }}">Last Updated: {{ last_modified_at | date: "%R" }} {{ tzn }} {{ last_modified_at | date: "%A, %e&nbsp;%B&nbsp;%Y" }}</p>
{% endif %}

<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
        <link href="https://api.mapbox.com/mapbox-gl-js/v2.2.0/mapbox-gl.css" rel="stylesheet">
        <script src="https://api.mapbox.com/mapbox-gl-js/v2.2.0/mapbox-gl.js"></script>
        <style>
        #map { 
            width: 100%; height: 400pt
        }
        .countdown {
            text-align:center;
            width:100%;
            background-color:#2B233D;
            color:white;
            padding:10px 20px;
        }
        .mapboxgl-popup-content {
            width: fit-content
        }
        .cell {
            margin: 5px;
            flex-grow: 1;
            flex-basis: 30%;
        }
        .flex-container {
            display:flex;
            flex-wrap: wrap;
            text-align: center;
        }
        @media (max-width: 800px) {
            .flex-container {
                flex-direction: column;
            }
            }
        .ptr-flex {
            display:flex;
            flex-wrap: wrap;
            text-align: center;
        }
        
        .ptr-cell {
            margin: 5px;
            flex-grow: 1;
            flex-basis: 20%;
        }
        @media (max-width: 700px) {
            .ptr-cell {
                margin: 5px;
                flex-grow: 1;
                flex-basis: 30%;
            }
            }
        @media (max-width: 600px) {
            .ptr-cell {
                margin: 5px;
                flex-grow: 1;
                flex-basis: 40%;
            }
            }
        @media (max-width: 400px) {
            .ptr-flex {
                flex-direction: column;
            }
            }
        </style>
    </head>
    <body>
        <!-- Load the `mapbox-gl-geocoder` plugin. -->
        <script src="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.0/mapbox-gl-geocoder.min.js"></script>
        <link rel="stylesheet" href="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-geocoder/v4.7.0/mapbox-gl-geocoder.css" type="text/css">
        
        <!-- Promise polyfill script is required -->
        <!-- to use Mapbox GL Geocoder in IE 11. -->
        <script src="https://cdn.jsdelivr.net/npm/es6-promise@4/dist/es6-promise.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/es6-promise@4/dist/es6-promise.auto.min.js"></script>

        <div id="map"></div>

        <script>
            mapboxgl.accessToken = 'pk.eyJ1Ijoiam9zaC1qdXN0am9zaCIsImEiOiJja3A2eHdmajIwNGFvMndtcmNsbnZycm44In0.SvsoxpdU7NRLYLVRFIu2kw';
            var map = new mapboxgl.Map({
                container: 'map',
                zoom: 0.3,
                center: [0, 20],
                style: 'mapbox://styles/mapbox/streets-v11'
            });

            // filters for classifying parkruns into five categories based on magnitude
            var parkrunning = ['==', ['get', 'Status'], 'parkrunning'];
            var juniorrunning = ['==', ['get', 'Status'], 'junior parkrunning'];
            var cancelled5k = ['==', ['get', 'Status'], '5k Cancellation'];
            var cancelled2k = ['==', ['get', 'Status'], 'junior Cancellation'];
            var ptr = ['==', ['get', 'Status'], 'PtR'];

            // colors to use for the categories
            var colors = ['#7CB342', '#0288D1', '#A52714', '#1A237E', '#F9A825'];

            map.on('load', function () {
                // add a clustered GeoJSON source for a sample set of parkruns
                map.addSource('parkruns', {
                    'type': 'geojson',
                    'data': {{ site.data.raw.events | jsonify}},
                    'cluster': true,
                    'clusterRadius': 50,
                    'clusterProperties': {
                        // keep separate counts for each magnitude category in a cluster
                        'parkrunning': ['+', ['case', parkrunning, 1, 0]],
                        'juniorrunning': ['+', ['case', juniorrunning, 1, 0]],
                        'cancelled5k': ['+', ['case', cancelled5k, 1, 0]],
                        'cancelled2k': ['+', ['case', cancelled2k, 1, 0]],
                        'ptr': ['+', ['case', ptr, 1, 0]],
                    }
                });
                // circle and symbol layers for rendering individual parkruns (unclustered points)
                map.addLayer({
                    'id': 'parkrun_circle',
                    'type': 'circle',
                    'source': 'parkruns',
                    'filter': ['!=', 'cluster', true],
                    'paint': {
                        'circle-color': [
                            'case',
                            parkrunning,
                            colors[0],
                            juniorrunning,
                            colors[1],
                            cancelled5k,
                            colors[2],
                            cancelled2k,
                            colors[3],
                            colors[4]
                        ],
                        'circle-opacity': 0.6,
                        'circle-radius': 12
                    }
                });
                map.addLayer({
                    'id': 'parkrun_label',
                    'type': 'symbol',
                    'source': 'parkruns',
                    'filter': ['!=', 'cluster', true],
                    'layout': {
                        'text-field': ['get', 'EventShortName'],
                        'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
                        'text-size': 12
                    },
                    'paint': {
                        'text-color': '#000000'
                    }
                });

                // objects for caching and keeping track of HTML marker objects (for performance)
                var markers = {};
                var markersOnScreen = {};

                function updateMarkers() {
                    var newMarkers = {};
                    var features = map.querySourceFeatures('parkruns');

                    // for every cluster on the screen, create an HTML marker for it (if we didn't yet),
                    // and add it to the map if it's not there already
                    for (var i = 0; i < features.length; i++) {
                        var coords = features[i].geometry.coordinates;
                        var props = features[i].properties;
                        if (!props.cluster) continue;
                        var id = props.cluster_id;

                        var marker = markers[id];
                        if (!marker) {
                            var el = createDonutChart(props);
                            marker = markers[id] = new mapboxgl.Marker({
                                element: el
                            }).setLngLat(coords);
                        }
                        newMarkers[id] = marker;

                        if (!markersOnScreen[id]) marker.addTo(map);
                    }
                    // for every marker we've added previously, remove those that are no longer visible
                    for (id in markersOnScreen) {
                        if (!newMarkers[id]) markersOnScreen[id].remove();
                    }
                    markersOnScreen = newMarkers;
                }

                // after the GeoJSON data is loaded, update markers on the screen on every frame
                map.on('render', function () {
                    if (!map.isSourceLoaded('parkruns')) return;
                    updateMarkers();
                });
                // When a click event occurs on a feature in the places layer, open a popup at the
                // location of the feature, with description HTML from its properties.
                map.on('click', 'parkrun_circle', function (e) {
                    var coordinates = e.features[0].geometry.coordinates.slice();
                    var description = e.features[0].properties.description;
                    
                    // Ensure that if the map is zoomed out such that multiple
                    // copies of the feature are visible, the popup appears
                    // over the copy being pointed to.
                    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
                }
                
                new mapboxgl.Popup()
                    .setLngLat(coordinates)
                    .setHTML(description)
                    .addTo(map);
                });
                
                // Change the cursor to a pointer when the mouse is over the places layer.
                map.on('mouseenter', 'parkrun_circle', function () {
                    map.getCanvas().style.cursor = 'pointer';
                });
                
                // Change it back to a pointer when it leaves.
                map.on('mouseleave', 'parkrun_circle', function () {
                    map.getCanvas().style.cursor = '';
                });
            });

            // code for creating an SVG donut chart from feature properties
            function createDonutChart(props) {
                var offsets = [];
                var counts = [
                    props.parkrunning,
                    props.juniorrunning,
                    props.cancelled5k,
                    props.cancelled2k,
                    props.ptr
                ];
                var total = 0;
                for (var i = 0; i < counts.length; i++) {
                    offsets.push(total);
                    total += counts[i];
                }
                var fontSize =
                    total >= 1000 ? 22 : total >= 100 ? 20 : total >= 10 ? 18 : 16;
                var r = total >= 1000 ? 50 : total >= 100 ? 32 : total >= 10 ? 24 : 18;
                var r0 = Math.round(r * 0.6);
                var w = r * 2;

                var html =
                    '<div><svg width="' +
                    w +
                    '" height="' +
                    w +
                    '" viewbox="0 0 ' +
                    w +
                    ' ' +
                    w +
                    '" text-anchor="middle" style="font: ' +
                    fontSize +
                    'px sans-serif; display: block">';

                for (i = 0; i < counts.length; i++) {
                    html += donutSegment(
                        offsets[i] / total,
                        (offsets[i] + counts[i]) / total,
                        r,
                        r0,
                        colors[i]
                    );
                }
                html +=
                    '<circle cx="' +
                    r +
                    '" cy="' +
                    r +
                    '" r="' +
                    r0 +
                    '" fill="white" /><text dominant-baseline="central" transform="translate(' +
                    r +
                    ', ' +
                    r +
                    ')">' +
                    total.toLocaleString() +
                    '</text></svg></div>';

                var el = document.createElement('div');
                el.innerHTML = html;
                return el.firstChild;
            }

            function donutSegment(start, end, r, r0, color) {
                if (end - start === 1) end -= 0.00001;
                var a0 = 2 * Math.PI * (start - 0.25);
                var a1 = 2 * Math.PI * (end - 0.25);
                var x0 = Math.cos(a0),
                    y0 = Math.sin(a0);
                var x1 = Math.cos(a1),
                    y1 = Math.sin(a1);
                var largeArc = end - start > 0.5 ? 1 : 0;

                return [
                    '<path d="M',
                    r + r0 * x0,
                    r + r0 * y0,
                    'L',
                    r + r * x0,
                    r + r * y0,
                    'A',
                    r,
                    r,
                    0,
                    largeArc,
                    1,
                    r + r * x1,
                    r + r * y1,
                    'L',
                    r + r0 * x1,
                    r + r0 * y1,
                    'A',
                    r0,
                    r0,
                    0,
                    largeArc,
                    0,
                    r + r0 * x0,
                    r + r0 * y0,
                    '" fill="' + color + '" />'
                ].join(' ');
            }
            // Add the control to the map.
            map.addControl(
                new MapboxGeocoder({
                    accessToken: mapboxgl.accessToken,
                    mapboxgl: mapboxgl
                })
            );
            map.addControl(new mapboxgl.NavigationControl());
            map.addControl(new mapboxgl.FullscreenControl());
        </script>
        <br />
        <h2>parkrun returns in:</h2>
        <script>let options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZoneName: 'short', hour:'2-digit', minute:'2-digit'};</script>
        <div class="flex-container">
            <div class="cell">
                <div class="countdown">
                    <!-- Display the timer timer in an element -->
                    <h3 style="margin:inherit; color:inherit">South Africa</h3>
                    <h2 id="timer2" style="margin:inherit; color:inherit;"></h2>
                    <p id="endDate2" style="margin:inherit;"></p>

                    <script>
                        // Set the date we're counting down to
                        var countDownDate2 = new Date( "2021/05/29 09:00:00 GMT+02:00").getTime();

                        // Update the count down every 1 second
                        var x = setInterval(function() {

                        // Get today's date and time
                        var now = new Date().getTime();

                        // Find the distance between now and the count down date
                        var distance = countDownDate2 - now;

                        // Time calculations for days, hours, minutes and seconds
                        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

                        // Display the result in the element with id="timer"
                        document.getElementById("timer2").innerHTML = days + "d " + hours + "h "
                        + minutes + "m " + seconds + "s ";

                        // If the count down is finished, write some text
                        if (distance < 0) {
                            clearInterval(x);
                            document.getElementById("timer2").innerHTML = "parkrun's Back!";
                        }
                        }, 1000);

                        var cdinput2 = new Date(countDownDate2)

                        var cdoutput2 = cdinput2.toLocaleString('default', options);

                        document.getElementById("endDate2").innerHTML = cdoutput2
                    </script>
                </div>
            </div>
            <div class="cell">
                <div class="countdown">
                    <!-- Display the timer timer in an element -->
                    <h3 style="margin:inherit; color:inherit">Poland</h3>
                    <h2 id="timer3" style="margin:inherit; color:inherit;"></h2>
                    <p id="endDate3" style="margin:inherit;"></p>

                    <script>
                        // Set the date we're counting down to
                        var countDownDate3 = new Date( "2021/06/12 09:00:00 GMT+02:00").getTime();

                        // Update the count down every 1 second
                        var x = setInterval(function() {

                        // Get today's date and time
                        var now = new Date().getTime();

                        // Find the distance between now and the count down date
                        var distance = countDownDate3 - now;

                        // Time calculations for days, hours, minutes and seconds
                        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

                        // Display the result in the element with id="timer"
                        document.getElementById("timer3").innerHTML = days + "d " + hours + "h "
                        + minutes + "m " + seconds + "s ";

                        // If the count down is finished, write some text
                        if (distance < 0) {
                            clearInterval(x);
                            document.getElementById("timer3").innerHTML = "parkrun's Back!";
                        }
                        }, 1000);

                        var cdinput3 = new Date(countDownDate3)

                        var cdoutput3 = cdinput3.toLocaleString('default', options);

                        document.getElementById("endDate3").innerHTML = cdoutput3
                    </script>
                </div>
            </div>
            <div class="cell">
                <div class="countdown" style="background-color:#00ceae">
                    <!-- Display the timer timer in an element -->
                    <h3 style="margin:inherit; color:inherit">Scotland (juniors)</h3>
                    <h2 id="timer4" style="margin:inherit; color:inherit;"></h2>
                    <p id="endDate4" style="margin:inherit;"></p>

                    <script>
                        // Set the date we're counting down to
                        var countDownDate4 = new Date( "2021/06/20 09:00:00 GMT+01:00").getTime();

                        // Update the count down every 1 second
                        var x = setInterval(function() {

                        // Get today's date and time
                        var now = new Date().getTime();

                        // Find the distance between now and the count down date
                        var distance = countDownDate4 - now;

                        // Time calculations for days, hours, minutes and seconds
                        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

                        // Display the result in the element with id="timer"
                        document.getElementById("timer4").innerHTML = days + "d " + hours + "h "
                        + minutes + "m " + seconds + "s ";

                        // If the count down is finished, write some text
                        if (distance < 0) {
                            clearInterval(x);
                            document.getElementById("timer4").innerHTML = "parkrun's Back!";
                        }
                        }, 1000);

                        var cdinput4 = new Date(countDownDate4)

                        var cdoutput4 = cdinput4.toLocaleString('default', options);

                        document.getElementById("endDate4").innerHTML = cdoutput4
                    </script>
                </div>
            </div> 
            <div class="cell">
                <div class="countdown">
                    <h3 style="margin:inherit; color:inherit">England* and Northern Ireland</h3>
                    <h2 id="timer1" style="margin:inherit; color:inherit;"></h2>
                    <p id="endDate1" style="margin:inherit;"></p>

                    <script>
                        // Set the date we're counting down to
                        var countDownDate1 = new Date("Jun 26, 2021 09:00:00 GMT+01:00").getTime();

                        // Update the count down every 1 second
                        var x = setInterval(function() {

                        // Get today's date and time
                        var now = new Date().getTime();

                        // Find the distance between now and the count down date
                        var distance = countDownDate1 - now;

                        // Time calculations for days, hours, minutes and seconds
                        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

                        // Display the result in the element with id="timer1"
                        document.getElementById("timer1").innerHTML = days + "d " + hours + "h "
                        + minutes + "m " + seconds + "s ";

                        // If the count down is finished, write some text
                        if (distance < 0) {
                            clearInterval(x);
                            document.getElementById("timer1").innerHTML = "parkrun's Back!";
                        }
                        }, 1000);

                        var cdinput1 = new Date(countDownDate1)

                        var cdoutput1 = cdinput1.toLocaleString('default', options);

                        document.getElementById("endDate1").innerHTML = cdoutput1
                    </script>
                </div>

                <p style="text-align: center;">* Dependent on a substantial number of events returning. You can read more about that <a href="https://blog.josh.me.uk/2021/05/12/update-to-the-parkrun-cancellations-map/">here</a>.</p>
            </div>
            <div class="cell">
                <div class="countdown">
                    <!-- Display the timer timer in an element -->
                    <h3 style="margin:inherit; color:inherit">Scotland</h3>
                    <h2 id="timer5" style="margin:inherit; color:inherit;"></h2>
                    <p id="endDate5" style="margin:inherit;"></p>

                    <script>
                        // Set the date we're counting down to
                        var countDownDate5 = new Date( "2021/07/03 09:00:00 GMT+01:00").getTime();

                        // Update the count down every 1 second
                        var x = setInterval(function() {

                        // Get today's date and time
                        var now = new Date().getTime();

                        // Find the distance between now and the count down date
                        var distance = countDownDate5 - now;

                        // Time calculations for days, hours, minutes and seconds
                        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

                        // Display the result in the element with id="timer"
                        document.getElementById("timer5").innerHTML = days + "d " + hours + "h "
                        + minutes + "m " + seconds + "s ";

                        // If the count down is finished, write some text
                        if (distance < 0) {
                            clearInterval(x);
                            document.getElementById("timer5").innerHTML = "parkrun's Back!";
                        }
                        }, 1000);

                        var cdinput5 = new Date(countDownDate5)

                        var cdoutput5 = cdinput5.toLocaleString('default', options);

                        document.getElementById("endDate5").innerHTML = cdoutput5
                    </script>
                </div>
            </div>
        </div>

        <h3> The following English events have been granted permission to return </h3>

        <div class="ptr-flex">
            {% for row in site.data.PtR %}
                {% unless forloop.first %}
                    {% tablerow pair in row %}
                       <div class="ptr-cell">{{ pair[1] }}</div>
                    {% endtablerow %}
                {% endunless %}
            {% endfor %}
        </div>
    </body>
</html>
