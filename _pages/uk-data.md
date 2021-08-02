---
layout: page
title: UK Data
tag: parkrun
date: 2021-05-27
permalink: /more-uk
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
    var out = lm_date.toLocaleString('defalit', options);
    document.getElementById("lastupdated").innerHTML = 'Data Last Refreshed: ' + out
</script>

<style>
    #contents {
        width: max-content;
        border: 1px solid #a2a9b1;
        background-color: #f8f9fa;
        padding: 5px;
        font-size: 95%;
    }
    #contents h3 {
        margin-top: 0;
    }
    #contents li {
        padding-right: 30px
    }
</style>

<div id='contents' role='navigation'>
<h3>Contents</h3>
    <ul>
        <li><a href="#summary">Summary</a></li>
        <li><a href="#england">England</a></li>
        <li><a href="#ni">Northern Ireland</a></li>
        <li><a href="#scotland">Scotland</a></li>
        <li><a href="#wales">Wales</a></li>
    </ul>
</div>
<div id='summary'>
<h2 class="split">Summary</h2>
<p>Below is a summary of the UK Data broken down by constituent country.</p>
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
<p>'Other' includes parkruns in the Falkland Islands and the <a href="https://en.wikipedia.org/wiki/Crown_Dependencies">Crown Dependencies</a>.</p>
<p style="text-align:end"><a href="#contents">back to the top</a></p>
</div>
<div id='england'>
<h2 class="split">England</h2>
<div class="hscrollable">
    <table style="width: 100%;">
        <tr>
            <th>County</th>
            <th>parkrunning</th>
            <th>junior parkrunning</th>
            <th>5k Cancellations</th>
            <th>junior Cancellations</th>
            <th>Total</th>
        </tr>
        {% for row in site.data.parkrun.counties.england %}
            <tr>
                {% unless forloop.last %}
                    <td>{{ row['County'] }}</td>
                    <td>{{ row['parkrunning'] }}</td>
                    <td>{{ row['junior parkrunning'] }}</td>
                    <td>{{ row['5k Cancellations'] }}</td>
                    <td>{{ row['junior Cancellations'] }}</td>
                    <td>{{ row['Total'] }}</td>
                <!--</tr>
                <tr>
                    <td></td>
                    <td>{% assign var = row['5k Events Running'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['junior Events Running'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['5k Events Cancelled'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['junior Events Cancelled'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td></td>-->
                {% else %}
                    <th>{{ row['County'] }}</th>
                    <th>{{ row['parkrunning'] }}</th>
                    <th>{{ row['junior parkrunning'] }}</th>
                    <th>{{ row['5k Cancellations'] }}</th>
                    <th>{{ row['junior Cancellations'] }}</th>
                    <th>{{ row['Total'] }}</th>
                {% endunless %}
            </tr>
        {% endfor %}
    </table>
</div>
<p style="text-align:end"><a href="#contents">back to the top</a></p>
</div>
<div id='ni'>
<h2 class="split">Northern Ireland</h2>
<div class="hscrollable">
    <table style="width: 100%;">
        <tr>
            <th>County</th>
            <th>parkrunning</th>
            <th>junior parkrunning</th>
            <th>5k Cancellations</th>
            <th>junior Cancellations</th>
            <th>Total</th>
        </tr>
        {% for row in site.data.parkrun.counties.ni %}
            <tr>
                {% unless forloop.last %}
                    <td>{{ row['County'] }}</td>
                    <td>{{ row['parkrunning'] }}</td>
                    <td>{{ row['junior parkrunning'] }}</td>
                    <td>{{ row['5k Cancellations'] }}</td>
                    <td>{{ row['junior Cancellations'] }}</td>
                    <td>{{ row['Total'] }}</td>
                <!--</tr>
                <tr>
                    <td></td>
                    <td>{% assign var = row['5k Events Running'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['junior Events Running'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['5k Events Cancelled'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['junior Events Cancelled'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td></td>-->
                {% else %}
                    <th>{{ row['County'] }}</th>
                    <th>{{ row['parkrunning'] }}</th>
                    <th>{{ row['junior parkrunning'] }}</th>
                    <th>{{ row['5k Cancellations'] }}</th>
                    <th>{{ row['junior Cancellations'] }}</th>
                    <th>{{ row['Total'] }}</th>
                {% endunless %}
            </tr>
        {% endfor %}
    </table>
</div>
<p style="text-align:end"><a href="#contents">back to the top</a></p>
</div>
<div id='scotland'>
<h2 class="split">Scotland</h2>
<div class="hscrollable">
    <table style="width: 100%;">
        <tr>
            <th>County</th>
            <th>parkrunning</th>
            <th>junior parkrunning</th>
            <th>5k Cancellations</th>
            <th>junior Cancellations</th>
            <th>Total</th>
        </tr>
        {% for row in site.data.parkrun.counties.scotland %}
            <tr>
                {% unless forloop.last %}
                    <td>{{ row['County'] }}</td>
                    <td>{{ row['parkrunning'] }}</td>
                    <td>{{ row['junior parkrunning'] }}</td>
                    <td>{{ row['5k Cancellations'] }}</td>
                    <td>{{ row['junior Cancellations'] }}</td>
                    <td>{{ row['Total'] }}</td>
                <!--</tr>
                <tr>
                    <td></td>
                    <td>{% assign var = row['5k Events Running'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['junior Events Running'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['5k Events Cancelled'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['junior Events Cancelled'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td></td>-->
                {% else %}
                    <th>{{ row['County'] }}</th>
                    <th>{{ row['parkrunning'] }}</th>
                    <th>{{ row['junior parkrunning'] }}</th>
                    <th>{{ row['5k Cancellations'] }}</th>
                    <th>{{ row['junior Cancellations'] }}</th>
                    <th>{{ row['Total'] }}</th>
                {% endunless %}
            </tr>
        {% endfor %}
    </table>
</div>
<p style="text-align:end"><a href="#contents">back to the top</a></p>
</div>
<div id='wales'>
<h2 class="split">Wales</h2>
<div class="hscrollable">
    <table style="width: 100%;">
        <tr>
            <th>County</th>
            <th>parkrunning</th>
            <th>junior parkrunning</th>
            <th>5k Cancellations</th>
            <th>junior Cancellations</th>
            <th>Total</th>
        </tr>
        {% for row in site.data.parkrun.counties.wales %}
            <tr>
                {% unless forloop.last %}
                    <td>{{ row['County'] }}</td>
                    <td>{{ row['parkrunning'] }}</td>
                    <td>{{ row['junior parkrunning'] }}</td>
                    <td>{{ row['5k Cancellations'] }}</td>
                    <td>{{ row['junior Cancellations'] }}</td>
                    <td>{{ row['Total'] }}</td>
                <!--</tr>
                <tr>
                    <td></td>
                    <td>{% assign var = row['5k Events Running'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['junior Events Running'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['5k Events Cancelled'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td>{% assign var = row['junior Events Cancelled'] | split: "|" | sort %}{% for i in var %}{{ i }}{% unless forloop.last %}<br/>{% endunless %}{% endfor %}</td>
                    <td></td>-->
                {% else %}
                    <th>{{ row['County'] }}</th>
                    <th>{{ row['parkrunning'] }}</th>
                    <th>{{ row['junior parkrunning'] }}</th>
                    <th>{{ row['5k Cancellations'] }}</th>
                    <th>{{ row['junior Cancellations'] }}</th>
                    <th>{{ row['Total'] }}</th>
                {% endunless %}
            </tr>
        {% endfor %}
    </table>
</div>
<p style="text-align:end"><a href="#contents">back to the top</a></p>
</div>
