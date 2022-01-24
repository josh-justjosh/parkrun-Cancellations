---
layout: page
title: UK and Ireland Data
tag: parkrun
date: 2021-05-27
permalink: /more-uk-ie
---

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

[Back to the 'more info' page](/more)

<div id='contents' role='navigation'>
<h3>Contents</h3>
    <ul>
        <li><a href="#uk summary">UK Summary</a></li>
        <ul>
            <li><a href="#england">England</a></li>
            <li><a href="#ni">Northern Ireland</a></li>
            <li><a href="#scotland">Scotland</a></li>
            <li><a href="#wales">Wales</a></li>
        </ul>
        <li><a href="#ireland">Ireland</a></li>
    </ul>
</div>
<div id='uk summary'>
<h2 class="split">UK Summary</h2>
<p>Below is a summary of the UK Data broken down by constituent country.</p>
<div class="hscrollable">
    <table style="width: 100%;">
        {% for row in site.data.uk-data %}
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
<p>Below is the data for english parkruns broken down by <a href="https://en.wikipedia.org/wiki/Ceremonial_counties_of_England">ceremonial counties</a>.</p>
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
        {% for row in site.data.counties.england %}
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
<p>Below is the data for northern irish parkruns broken down by <a href="https://en.wikipedia.org/wiki/Counties_of_Northern_Ireland">counties</a> with Belfast split out.</p>
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
        {% for row in site.data.counties.ni %}
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
<p>Below is the data for scottish parkruns broken down by <a href="https://en.wikipedia.org/wiki/Lieutenancy_areas_of_Scotland">lieutenancy areas</a>.</p>
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
        {% for row in site.data.counties.scotland %}
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
<p>Below is the data for welsh parkruns broken down by <a href="https://en.wikipedia.org/wiki/Preserved_counties_of_Wales">preserved counties</a>.</p>
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
        {% for row in site.data.counties.wales %}
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
<div id='ireland'>
<h2 class="split">Ireland</h2>
<p>Below is the data for irish parkruns broken down by <a href="https://en.wikipedia.org/wiki/Counties_of_Ireland">counties</a>.</p>
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
        {% for row in site.data.counties.ireland %}
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
