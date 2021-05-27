---
layout: page
title: parkrun Cancellations
permalink: /parkrun-cancellations-may2021-testing/
date: 2021-05-27 22:06 +0100
tag: parkrun
published: false
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
  <p class="author_title" datetime="{{ last_modified_at | date_to_xmlschema }}">Last Updated: {{ last_modified_at | date: "%R %A, %e&nbsp;%B&nbsp;%Y" }} {{ tzn }}</p>
{% endif %}

{% google_map src="_data/events" width="100%" %}

<div style="text-align: center;">
    <iframe src="https://free.timeanddate.com/countdown/i7q1ask7/n1325/cf100/cm0/cu4/ct0/cs0/ca0/cr0/ss0/cacfff/cpcfff/pc2b233d/tc66c/fs200/szw448/szh189/tatparkrun%20Returns%2a/tacfff/tptparkrun%20is%20Back!/tpcfff/mat(in%20England)/macfff/mpt%20(in%20England)/mpcfff/iso2021-06-26T09:00:00" allowtransparency="true" frameborder="0" width="448" height="189"></iframe>
</div>

<p style="text-align: center;">* Dependent on a substantial number of events returning. You can read more about that <a href="https://blog.josh.me.uk/2021/05/12/update-to-the-parkrun-cancellations-map/">here</a>.

<h2> The following events have been granted permission to return </h2>

<table style="margin-left:auto; margin-right:auto;">
  {% for row in site.data.PtRtable %}
    {% unless forloop.first %}
    {% tablerow pair in row %}
      {{ pair[1] }}
    {% endtablerow %}
    {% endunless %}
  {% endfor %}
</table>
