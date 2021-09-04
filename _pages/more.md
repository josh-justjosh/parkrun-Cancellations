---
layout: page
title: More Info
tag: parkrun
date: 2021-05-27
permalink: /more
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
<div style="background-color: rgba(255,128,0,0.25); margin: 25px; padding: 10px; text-align: center">
    <p>These pages are in beta, please see <a href="#contact">the information at the bottom of the page</a> for how to report errors.<br />You should always check the event's website and social media channels before setting out.</p>
</div>

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
            display: flex;
            flex-direction: column;
            height: 100%;
            justify-content: center;
        }
        .mapboxgl-popup-content {
            width: fit-content
        }
        .flex-item {
            margin: 5px;
            flex-grow: 1;
            flex-basis: 48%;
        }
        .flex-container {
            display:flex;
            flex-wrap: wrap;
            text-align: center;
        }
        .flex-key {
            margin: 10px 5px;
            flex-grow: 1;
        }
        .flex-key p {
            margin: 0;
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
        .collapsible, .collapsiblecan, .collapsiblerein, .collapsiblestatus, .collapsiblestats {
            background-color: #2B233D;
            color: white;
            cursor: pointer;
            padding: 18px;
            width: -webkit-fill-available;
            width: -moz-available;
            border: none;
            text-align: left;
            outline: none;
            font-size: 15px;
            }
        .active, .collapsible:hover, .collapsiblecan:hover, .collapsiblerein:hover, .collapsiblestatus:hover, .collapsiblestats:hover {
            background-color: #14101d;
            }
        .expcontent, .expcontentcan, .expcontentrein, .expcontentstatus, .expcontentstats {
            padding: 0 18px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.5s ease-out;
            }
        </style>
    </head>
    <body>
        <script>
            const queryString = window.location.search;
            const urlParams = new URLSearchParams(queryString);
            const zoom = urlParams.get('zoom')
            //console.log(zoom);
            const lat = urlParams.get('lat')
            //console.log(lat);
            const long = urlParams.get('long')
            //console.log(long);
            const center = [long,lat]
            //console.log(center);
        </script>
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
            if (zoom != null && lat != null && long != null) {
                var map = new mapboxgl.Map({
                    container: 'map',
                    zoom: zoom,
                    center: center,
                    style: 'mapbox://styles/mapbox/streets-v11'
                });
            } else if (zoom != null && lat == null && long == null) {
                var map = new mapboxgl.Map({
                    container: 'map',
                    zoom: zoom,
                    center: [10, 20],
                    style: 'mapbox://styles/mapbox/streets-v11'
                });
            } else if (zoom == null && lat != null && long != null) { 
                var map = new mapboxgl.Map({
                    container: 'map',
                    zoom: 0.9,
                    center: center,
                    style: 'mapbox://styles/mapbox/streets-v11'
                });   
            } else {
                var map = new mapboxgl.Map({
                    container: 'map',
                    zoom: 0.9,
                    center: [10, 20],
                    style: 'mapbox://styles/mapbox/streets-v11'
                });
            }
            // filters for classifying parkruns into five categories based on value
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
                    'data': {{ site.data.parkrun.events | jsonify}},
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
                // after the GeoJSON data are loaded, update markers on the screen on every frame
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
            var ourGeoLocator = new mapboxgl.GeolocateControl({
                positionOptions: {
                enableHighAccuracy: false
                },
                fitBoundsOptions: {
                maxZoom: 10
                }
            })
            map.addControl(ourGeoLocator);
            map.addControl(new mapboxgl.NavigationControl({showCompass: false}));
            map.addControl(new mapboxgl.FullscreenControl());
            // disable map rotation using right click + drag
            map.dragRotate.disable();
            // disable map rotation using touch rotation gesture
            map.touchZoomRotate.disableRotation();
            // Center the map on the coordinates of any clicked circle from the 'parkrun_circle' layer.
            map.on('click', 'parkrun_circle', function (e) {
                map.flyTo({
                center: e.features[0].geometry.coordinates
                });
            });
        </script>
        <style>
                /* The switch - the box around the slider */
        .switch {
            position: sticky;
            display: inline-block;
            width: 60px;
            height: 34px;
        }
        /* Hide default HTML checkbox */
        .switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        /* The slider */
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #ccc;
            -webkit-transition: .4s;
            transition: .4s;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 26px;
            width: 26px;
            left: 4px;
            bottom: 4px;
            background-color: white;
            -webkit-transition: .4s;
            transition: .4s;
        }
        input:checked + .slider#switch1 {
            background-color: #7CB342;
        }
        input:checked + .slider#switch2 {
            background-color: #0288D1;
        }
        input:checked + .slider#switch3 {
            background-color: #A52714;
        }
        input:checked + .slider#switch4 {
            background-color: #1A237E;
        }
        input:checked + .slider#switch5 {
            background-color: #F9A825;
        }
        input:focus + .slider {
            box-shadow: 0 0 1px #2196F3;
        }
        input:checked + .slider:before {
            -webkit-transform: translateX(26px);
            -ms-transform: translateX(26px);
            transform: translateX(26px);
        }
        /* Rounded sliders */
        .slider.round {
            border-radius: 34px;
        }
        .slider.round:before {
            border-radius: 50%;
        }
        </style>
        <div class="flex-container" style="color: #FFFFFF">
            <div class="flex-key">
                <p id="key1">parkrunning</p>
                <!--<label class="switch"><input type="checkbox" id="check1" checked onclick="toggleparkruns()"><span class="slider round" id="switch1"></span></label>
                <p id="text" style="display:block; color: #000000">CHECKED!</p>-->
            </div>
            <div class="flex-key">
                <p id="key2">junior parkrunning</p>
                <!--<label class="switch"><input type="checkbox" id="check2" checked><span class="slider round" id="switch2"></span></label>-->
            </div>
            <div class="flex-key">
                <p id="key3">5k Cancellations</p>
                <!--<label class="switch"><input type="checkbox" id="check3" checked><span class="slider round" id="switch3"></span></label>-->
            </div>
            <div class="flex-key">
                <p id="key4">junior Cancellations</p>
                <!--<label class="switch"><input type="checkbox" id="check4" checked><span class="slider round" id="switch4"></span></label>-->
            </div>
            <!--<div class="flex-key">
                <p id="key5">Permission to Return Received</p>
                <!--<label class="switch"><input type="checkbox" id="check5" checked><span class="slider round" id="switch5"></span></label>--
            </div>-->
        </div>
        <script>
            document.getElementById('key1').style.backgroundColor = colors[0] ;
            document.getElementById('key2').style.backgroundColor = colors[1] ;
            document.getElementById('key3').style.backgroundColor = colors[2] ;
            document.getElementById('key4').style.backgroundColor = colors[3] ;
            //document.getElementById('key5').style.backgroundColor = colors[4] ;
            function toggleparkruns() {
                var checkBox = document.getElementById("check1");
                var text = document.getElementById("text");
                if (checkBox.checked == true){
                    text.style.display = "block";
                } else {
                    text.style.display = "none";
                }
            }
        </script>
        <div style="display:flex; flex-wrap: wrap;">
        <p style="flex-grow: 1;">Showing data for 
        {% for row in site.data.parkrun.cancellation-dates %}
            {% for pair in row %}
                {% for item in pair %}
                    {% if forloop.last %}
                        and 
                    {% endif %}
                    {{ item | date: "%A, %e&nbsp;%B&nbsp;%Y" }}
                {% endfor %}
            {% endfor %}
        {% endfor %}
        </p>
        <a style="margin:auto; flex-grow: 1; text-align: end;" href="/" id="map-link">Click here to go to the full map.</a>
        </div>
        {% if site.data.parkrun.cancellation-changes.size > 0 %}
        <h2 class="split">Most Recent Changes</h2>
            <div>
                {% if site.data.parkrun.cancellation-additions.size > 0 %}
                    <button type="button" class="collapsiblecan" style="margin: 5px;"><p style="float:left; margin: 0">Click to view the most recent Cancellations</p><p style="float:right; margin: 0" id='lastaddition'>Last Change: {{site.data.parkrun.cancellation-additions.last.Event | date: "%R UTC %A, %e&nbsp;%B&nbsp;%Y" }}</p></button>
                    <div class="expcontentcan">
                        <div class="hscrollable">
                            <table style="width: 100%">
                                <tr>
                                    <th>Event</th>
                                    <th>Country</th>
                                    <th>Cancellation Note</th>
                                </tr>
                                {% for row in site.data.parkrun.cancellation-additions %}
                                    {% unless forloop.last %}
                                    <tr>
                                        {% if row['Website'] != null %}
                                        <td><a href="{{ row['Website'] }}">{{ row['Event'] }}</a></td>
                                        {% else %}
                                        <td>{{ row['Event'] }}</td>
                                        {% endif %}
                                        <td>{{ row['Country'] }}</td>
                                        <td>{{ row['Cancellation Note'] }}</td>
                                    </tr>
                                    {% endunless %}
                                {% endfor %}
                            </table>
                        </div>
                        <a href="/updates" style="float:right">Click to see a full history</a>
                    </div>
                    <script>
                        var last_addition = new Date("{{ site.data.parkrun.cancellation-additions.last.Event }} UTC").getTime();
                        var la_date = new Date(last_addition)
                        var outa = la_date.toLocaleString('default', options);
                        document.getElementById("lastaddition").innerHTML = 'Last Change: ' + outa
                        var coll = document.getElementsByClassName("collapsiblecan");
                        var i;
                        for (i = 0; i < coll.length; i++) {
                        coll[i].addEventListener("click", function() {
                            this.classList.toggle("active");
                            var expcontentcan = this.nextElementSibling;
                            if (expcontentcan.style.maxHeight){
                            expcontentcan.style.maxHeight = null;
                            } else {
                            expcontentcan.style.maxHeight = expcontentcan.scrollHeight + "px";
                            } 
                        });
                        }
                    </script>
                {% endif %}
            </div>
            <!--<div>
                {% if site.data.parkrun.cancellation-removals.size > 0 %}
                    <button type="button" class="collapsiblerein" style="margin: 5px;"><p style="float:left; margin: 0">Click to view the most recent Reinstatements</p><p style="float:right; margin: 0">Last Change: {{site.data.parkrun.cancellation-removals.last.Event | date: "%R UTC %A, %e&nbsp;%B&nbsp;%Y" }}</p></button>
                    <div class="expcontentrein">
                        <div class="hscrollable">
                           <table style="width: 100%">
                                <tr>
                                    <th>Event</th>
                                    <th>Country</th>
                                    <th>Cancellation Note</th>
                                </tr>
                                {% for row in site.data.parkrun.cancellation-removals %}
                                    {% unless forloop.last %}
                                    <tr>
                                        {% if row['Website'] != null %}
                                        <td><a href="{{ row['Website'] }}">{{ row['Event'] }}</a></td>
                                        {% else %}
                                        <td>{{ row['Event'] }}</td>
                                        {% endif %}
                                        <td>{{ row['Country'] }}</td>
                                        <td>{{ row['Cancellation Note'] }}</td>
                                    </tr>
                                    {% endunless %}
                                {% endfor %}
                            </table>
                        </div>
                    </div>
                    <script>
                        var coll = document.getElementsByClassName("collapsiblerein");
                        var i;
                        for (i = 0; i < coll.length; i++) {
                        coll[i].addEventListener("click", function() {
                            this.classList.toggle("active");
                            var expcontentrein = this.nextElementSibling;
                            if (expcontentrein.style.maxHeight){
                            expcontentrein.style.maxHeight = null;
                            } else {
                            expcontentrein.style.maxHeight = expcontentrein.scrollHeight + "px";
                            } 
                        });
                        }
                    </script>
                {% endif %}
            </div>-->
        {% endif %}
        <br />
        <!--<h2 class="split">parkrun returns in:</h2>
        <div class="flex-container">
            <div class="flex-item" id="Wales Countdown">
                <div class="countdown">
                    <!-- Display the timer timer in an element --
                    <h3 style="margin:inherit; color:inherit">Wales</h3>
                    <h2 id="timer7" style="margin:inherit; color:inherit;"></h2>
                    <p id="endDate7" style="margin:inherit;"></p>
                    <script>
                        // Set the date we're counting down to
                        var countDownDate7 = new Date( "2021/08/21 09:00:00 GMT+01:00").getTime();
                        // Update the count down every 1 second
                        var x = setInterval(function() {
                        // Get today's date and time
                        var now = new Date().getTime();
                        // Find the distance between now and the count down date
                        var distance = countDownDate7 - now;
                        // Time calculations for days, hours, minutes and seconds
                        var weeks = Math.floor(distance / (1000 * 60 * 60 * 24 * 7));
                        var days = Math.floor((distance % (1000 * 60 * 60 * 24 * 7)) / (1000 * 60 * 60 * 24));
                        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
                        // Display the result in the element with id="timer"
                        if (weeks == 0) {
                            if (days == 0) {
                                document.getElementById("timer7").innerHTML = hours + "h " + minutes + "m " + seconds + "s ";
                            }
                            else {
                                document.getElementById("timer7").innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
                            }
                        }
                        else {
                            document.getElementById("timer7").innerHTML = weeks + "w " + days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
                        }
                        // If the count down is finished, write some text
                        if (distance < 0) {
                            clearInterval(x);
                            document.getElementById("timer7").innerHTML = "parkrun's Back!";
                        }
                        }, 1000);
                        var cdinput7 = new Date(countDownDate7)
                        var cdoutput7 = cdinput7.toLocaleString('default', options);
                        document.getElementById("endDate7").innerHTML = cdoutput7
                    </script>
                </div>
            </div>
        </div>
        <br />-->
        <!--<button type="button" class="collapsible" style="margin: 5px;">Click to view the english events with permission to return</button>
        <div class="expcontent">
            <h3> The following English events have been granted permission to return </h3>
            <div class="ptr-flex">
                {% for row in site.data.parkrun.PtR %}
                    <div class="ptr-cell">{{ row["Event"] }}</div>
                {% endfor %}
            </div>
        </div>
        <script>
            var coll = document.getElementsByClassName("collapsible");
            var i;
            for (i = 0; i < coll.length; i++) {
            coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var expcontent = this.nextElementSibling;
                if (expcontent.style.maxHeight){
                expcontent.style.maxHeight = null;
                } else {
                expcontent.style.maxHeight = expcontent.scrollHeight + "px";
                } 
            });
            }
        </script>-->
        <style>
        .countrystatus, .statusgreen, .statusamber, .statusred, .statusblue {
            display: flex;
            flex-direction: column;
            height: 100%;
            justify-content: center;
        }
        .countrystatus * {
                margin: 0;
            }
        .countrystatus p, .countrystatus a , .countrystatus h3, .countrystatus h4 {
                color: white;
            }
        .countrystatus a {
                font-weight: bold;
            }
        .flex-status {
            margin: 5px;
            flex-grow: 1;
        }
        .statusgreen {
            background-color: rgb(124, 179, 66);
        }
        .statusamber {
            background-color: rgb(249, 168, 37);
        }
        .statusred {
            background-color: rgb(165, 39, 20);
        }
        .statusblue {
            background-color: rgb(0, 206, 174);
        }
        .grid {
            display: grid;
            text-align: center;
            grid-gap: 1rem;
            grid-auto-flow: dense
        }
        @media (min-width: 890px) {
            #countrystatuses {
                grid-template-columns: repeat(10, minmax(0, 1fr));
            }
            #countrystatuses > .countrystatus:not(#irelandstatus, #swedenstatus, #usastatus) {
                grid-column: span 2;
            }
            #irelandstatus {
                grid-column: span 4;
            }
            #swedenstatus {
                grid-column-start: 4;
                grid-column-end: 6;
            }
            #usastatus {
                grid-column-start: 6;
                grid-column-end: 8;
            }
        }
        @media (max-width: 890px) {
            #countrystatuses {
                grid-template-columns: repeat(4, minmax(0, 1fr));
            }
            #countrystatuses > .countrystatus:not(#irelandstatus, #swedenstatus, #usastatus) {
                grid-column: span 1;
            }
            #irelandstatus {
                grid-column: span 2;
            }
            #swedenstatus {
                grid-column-start: 2
            }
            #usastatus {
                grid-column-start: 3
            }
        }
        @media (max-width: 750px) {
            #countrystatuses {
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }
            #swedenstatus {
                grid-column-start: unset
            }
            #usastatus {
                grid-column-start: 2
            }
        }
        @media (max-width: 560px) {
            #countrystatuses {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
            #usastatus {
                grid-column-start: unset
            }
        }
        @media (min-width: 380px) {
            #irelandgrid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
            #irelandtitle {
                grid-column: span 2;
            }
        }
        @media (max-width: 380px) {
            #countrystatuses {
                grid-template-columns: repeat(1, minmax(0, 1fr));
            }
            #irelandstatus {
                grid-column: span 1;
            }
        }
        @media (min-width: 690px) {
            #australiagrid {
                grid-template-columns: repeat(4, minmax(0, 1fr));
            }
        }
        @media (max-width: 690px) {
            #australiagrid {
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }
        }
        @media (max-width: 550px) {
            #australiagrid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }
        #ukgrid, #englandgrid, #nigrid, #scotlandgrid, #walesgrid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
        @media (max-width: 900px) {
            #ukgrid {
                grid-template-columns: repeat(1, minmax(0, 1fr))
            }
        }
        </style>
        <button type="button" class="collapsiblestatus" style="margin: 5px;">Click to view a summary of the status of parkruns in each country</button>
        <div class="expcontent">
            <div class="grid">
                <div>
                    <h2 class="split">Country Situations</h2>
                    <p id="statusupdated">Last Updated*: {% capture statusupdated %}2021-09-04 07:38 UTC+1{% endcapture %}</p>
                    <script>
                        var statusupdated = new Date("{{statusupdated}}").getTime();
                        var su_date = new Date(statusupdated)
                        var out = su_date.toLocaleString('default', options);
                        document.getElementById("statusupdated").innerHTML = 'Last Updated*: ' + out
                    </script>
                </div>
                <div id="countrystatuses" class="grid">
                    <div id="austriastatus" class="countrystatus">
                        <div class="statusgreen">
                            <h3>Austria</h3>
                            <p id="austriadate">Event Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusamber">
                            <h3>Canada</h3>
                            <p>Some Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusgreen">
                            <h3>Denmark</h3>
                            <p>Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusred">
                            <h3>Eswatini</h3>
                            <p>Event Suspended</p>
                        </div>
                    </div>
                    <div id="finlandstatus" class="countrystatus">
                        <div class="statusgreen">
                            <h3>Finland</h3>
                            <p id="finlanddate">Events Open</p>
                        </div>
                        </div>
                    <div class="countrystatus">
                        <div class="statusgreen">
                            <h3>France</h3>
                            <p>Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusgreen">
                            <h3>Germany</h3>
                            <p>Most Events Open</p>
                        </div>
                    </div>
                    <div id ="irelandstatus" class="countrystatus">
                        <div id ="irelandgrid" class="grid">
                            <h3 id="irelandtitle" style="color: unset">Ireland</h3>
                            <div class="statusred">
                                <p>5k Events Suspended</p>
                            </div>
                            <div id="irlandjstatus" class="statusamber">
                                <p id="irelandjuniorevents">Some junior Events Open</p>
                            </div>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusamber">
                            <h3>Italy</h3>
                            <p>Some Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusamber">
                            <h3>Japan</h3>
                            <p>Some Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusred">
                            <h3>Malaysia</h3>
                            <p>Events Suspended</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusgreen">
                            <h3>Namibia</h3>
                            <p>Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusgreen">
                            <h3>Netherlands</h3>
                            <p>Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusgreen">
                            <h3>New Zealand</h3>
                            <p>Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusamber">
                            <h3>Norway</h3>
                            <p>Some Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusgreen">
                            <h3>Poland</h3>
                            <p>Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusgreen">
                            <h3>Russia</h3>
                            <p>Most Events Open</p>
                        </div>
                    </div>
                    <div class="countrystatus">
                        <div class="statusred">
                            <h3>Singapore</h3>
                            <p>Events Suspended</p>
                        </div>
                    </div>
                    <div id="sastatus" class="countrystatus">
                        <div class="statusamber">
                            <h3>South Africa</h3>
                            <p id="sadate">Some Events Open</p>
                        </div>
                    </div>
                    <div id="swedenstatus" class="countrystatus">
                        <div class="statusgreen">
                            <h3>Sweden</h3>
                            <p id="sweedendate">Events Open</p>
                        </div>
                    </div>
                    <div id="usastatus" class="countrystatus">
                        <div class="statusgreen">
                            <h3>USA</h3>
                            <p>Most Events Open</p>
                        </div>
                    </div>
                </div>
                <div id="australiastatuses">
                    <h3 class="split">Australia</h3>
                    <div id="australiagrid" class="grid">
                        <div class="countrystatus">
                            <div class="statusred">
                                <h4>Australian Capital Territory</h4>
                                <p>Events Suspended</p>
                            </div>
                        </div>
                        <div class="countrystatus">
                            <div class="statusred">
                                <h3>New South Wales</h3>
                                <p>Events Suspended</p>
                            </div>
                        </div>
                        <div class="countrystatus">
                            <div class="statusgreen">
                                <h4>Northern Territory</h4>
                                <p>Events Open</p>
                            </div>
                        </div>
                        <div class="countrystatus">
                            <div class="statusgreen">
                                <h3>Queensland</h3>
                                <p>Events Open</p>
                            </div>
                        </div>
                        <div class="countrystatus">
                            <div class="statusgreen">
                                <h4>South Australia</h4>
                                <p>Events Open</p>
                            </div>
                        </div>
                        <div class="countrystatus">
                            <div class="statusgreen">
                                <h4>Tasmania</h4>
                                <p>Events Open</p>
                            </div>
                        </div>
                        <div class="countrystatus">  
                            <div class="statusred">
                                <h3>Victoria</h3>
                                <p>Events Suspended</p>
                            </div>
                        </div>
                        <div id="wastatus" class="countrystatus">
                            <div class="statusgreen">
                                <h4>Western Australia</h4>
                                <p>Events Open</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="ukstatuses">
                    <h3 class="split">United Kingdom</h3>
                    <div id="ukgrid" class="grid">
                        <div class="countrystatus">
                            <div id="englandgrid" class="grid">
                                <h4 style="grid-column: span 2; color: unset">England</h4>
                                <div>
                                    <div class="statusgreen">
                                        <p>Most 5k Events Open</p>
                                    </div>
                                </div>
                                <div>
                                    <div class="statusblue">
                                        <p>Most junior Events Open</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="countrystatus">
                            <div id="nigrid" class="grid">
                                <h4 style="grid-column: span 2; color: unset">Northern Ireland</h4>
                                <div>
                                    <div class="statusgreen">
                                        <p>5k Events Open</p>
                                    </div>
                                </div>
                                <div>
                                    <div class="statusblue">
                                        <p>junior Events Open</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="countrystatus">
                            <div id="scotlandgrid" class="grid">
                                <h4 style="grid-column: span 2; color: unset">Scotland</h4>
                                <div id="scotland5kstatus">
                                    <div class="statusgreen">
                                        <p id="scotlanddate">Most 5k Events Open</p>
                                    </div>
                                </div>
                                <div>
                                    <div class="statusblue">
                                        <p>Most junior Events Open</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="countrystatus">
                            <div id="walesgrid" class="grid">
                                <h4 id="walestitle" style="color: unset; grid-column: span 2">Wales</h4>
                                <div class="statusgreen">
                                    <p id="walesdate">Most 5k Events Open</p>
                                </div>
                                <div>
                                    <div class="statusblue">
                                        <p>Most junior Events Open</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <p>* Please note that these indicators are maintained manually, it is provided as a quick way to see parkrun's status around the world but is not guaranteed to be correct as things can change at short notice.</p>
            </div>
        </div>
        <script>
            var coll = document.getElementsByClassName("collapsiblestatus");
            var i;
            for (i = 0; i < coll.length; i++) {
            coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var expcontent = this.nextElementSibling;
                if (expcontent.style.maxHeight){
                expcontent.style.maxHeight = null;
                } else {
                expcontent.style.maxHeight = expcontent.scrollHeight + "px";
                } 
            });
            }
        </script>
        <button type="button" class="collapsiblestats" style="margin: 5px;">Click to view a summary of the data for each country</button>
        <div class="expcontent">
            <h2 class="split">Events</h2>
            <div class="hscrollable">
            <table style="width: 100%;">
                {% for row in site.data.parkrun.countries-data %}
                    <tr>
                        {% if forloop.first %}
                            {% for pair in row %}
                                <th>{{ pair[0] }}</th>
                            {% endfor %}
                            </tr>
                            <tr>
                            {% for pair in row %}
                                <td>{{ pair[1] }}</td>
                            {% endfor %}
                        {% elsif forloop.last %}
                            {% for pair in row %}
                                <th>{{ pair[1] }}</th>
                            {% endfor %}
                        {% else %}
                            {% for pair in row %}
                                <td>{{ pair[1] }}</td>
                            {% endfor %}
                        {% endif %}
                    </tr>
                {% endfor %}
            </table>
            </div>
            <p style="text-align:end; margin: 0"><a href="/graphs/global">See these data as graphs</a></p>
            <h2 class="split">UK Events</h2>
            <div class="hscrollable">
            <table style="width: 100%;">
                {% for row in site.data.parkrun.uk-data %}
                    <tr>
                        {% if forloop.first %}
                            {% for pair in row %}
                                <th>{{ pair[0] }}</th>
                            {% endfor %}
                            </tr>
                            <tr>
                            {% for pair in row %}
                                <td>{{ pair[1] }}</td>
                            {% endfor %}
                        {% elsif forloop.last %}
                            {% for pair in row %}
                                <th>{{ pair[1] }}</th>
                            {% endfor %}
                        {% else %}
                            {% for pair in row %}
                                <td>{{ pair[1] }}</td>
                            {% endfor %}
                        {% endif %}
                    </tr>
                {% endfor %}
            </table>
            </div>
            <p style="text-align:end; margin: 0"><a href="/graphs/uk">See these data as graphs</a> • <a href='more-uk-ie'>See more UK Data</a></p>
            <h2 class="split">Australian Events</h2>
            <div class="hscrollable">
            <table style="width: 100%;">
                {% for row in site.data.parkrun.aus-data %}
                    <tr>
                        {% if forloop.first %}
                            {% for pair in row %}
                                <th>{{ pair[0] }}</th>
                            {% endfor %}
                            </tr>
                            <tr>
                            {% for pair in row %}
                                <td>{{ pair[1] }}</td>
                            {% endfor %}
                        {% elsif forloop.last %}
                            {% for pair in row %}
                                <th>{{ pair[1] }}</th>
                            {% endfor %}
                        {% else %}
                            {% for pair in row %}
                                <td>{{ pair[1] }}</td>
                            {% endfor %}
                        {% endif %}
                    </tr>
                {% endfor %}
            </table>
            </div>
            <p style="text-align:end; margin: 0"><a href="/graphs/aus">See these data as graphs</a></p>
        </div>
        <script>
            var coll = document.getElementsByClassName("collapsiblestats");
            var i;
            for (i = 0; i < coll.length; i++) {
            coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var expcontent = this.nextElementSibling;
                if (expcontent.style.maxHeight){
                expcontent.style.maxHeight = null;
                } else {
                expcontent.style.maxHeight = expcontent.scrollHeight + "px";
                } 
            });
            }
            </script>
    </body>
</html>

This page is automatically updated throughout the week with data for the upcoming weekend. The data are refreshed approximately every three hours except on Friday evenings and Saturday mornings when the page is updated hourly (6pm Friday to 9am Saturday). Please be aware that due to the unreliabity of GitHub actions triggered by a schedule, data are unlikely to be refreshed excatly on the hour. You should always check the event's website and social media channels before setting out.

<p id="contact">The methods for collecting and parsing the data are not perfect. If you notice something that doesn't look right - please let me know by <a href="https://github.com/josh-justjosh/parkrun-cancellations/issues/new">opening an issue</a> in the GitHub repo, <a href="https://twitter.com/intent/tweet?text=@_Josh_justJosh%20@prcancellations">on twitter</a> or <a href="mailto:hello@josh.me.uk?subject=Issue with parkrun Cancellations page">by email</a>.</p>
