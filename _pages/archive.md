---
layout: page
permalink: /archive
title: Posts Archive
---
<style>
  .monthfb {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    column-gap: 10px;
  }
  .day {
    flex-basis:0;
  }
</style>

<div id="archives">
  <section id="archive">
    {%for post in site.posts %}
    {% if forloop.first == true %}
    <h2 class="split" id="{{ post.date | date: '%Y' }}" style="text-align:left;">{{ post.date | date: '%Y' }}</h2>
    <ul>
      <h3 id="{{ post.date | date: '%Y%m' }}" style="text-align:left;">{{ post.date | date: '%B&nbsp;%Y' }}</h3>
      <div class="monthfb">
        <div class="day">
        <h4 id="{{ post.date | date: '%Y%m%d' }}" style="text-align:left;">{{ post.date | date: '%e&nbsp;%B' }}</h4>
        <ul>
          <div style="display:flex; flex-wrap: wrap;"><li style="flex-grow:1; margin: auto 0 auto;"><a href="{{ site.baseurl }}{{ post.url }}">{{post.title | remove: " UTC Update" | date: "%H:%M" | replace: " ", "&nbsp;" }}</a></li>{% if post.published == false %}<div class="post-unpublished" style="margin:0;flex-grow:1"><p style="margin:1px 0 1px auto; width:min-content; text-align:end;">Unpublished</p></div>{% elsif post.hidden == true %}<div class="post-unpublished" style="margin:0;flex-grow:1"><p style="margin:1px 0 1px auto; width:min-content; text-align:end;">Hidden</p></div>{% endif %}</div>
          {% endif %}
          {% unless post.next %}
          {% else %}
          {% capture day %}{{ post.date | date: '%e %B %Y' }}{% endcapture %}
          {% capture nday %}{{ post.next.date | date: '%e %B %Y' }}{% endcapture %}
          {% capture month %}{{ post.date | date: '%B %Y' }}{% endcapture %}
          {% capture nmonth %}{{ post.next.date | date: '%B %Y' }}{% endcapture %}
          {% capture year %}{{ post.date | date: '%Y' }}{% endcapture %}
          {% capture nyear %}{{ post.next.date | date: '%Y' }}{% endcapture %}
          {% if year != nyear %}
        </ul>
        </div>
      </div>
    </ul>
    <h2 class="split" id="{{ post.date | date: '%Y' }}" style="text-align:left;">{{ post.date | date: '%Y' }}</h2>
    <ul>
      <h3 id="{{ post.date | date: '%Y%m' }}" style="text-align:left;">{{ post.date | date: '%B&nbsp;%Y' }}</h3>
      <div class="monthfb">
        <div class="day">
        <h4 id="{{ post.date | date: '%Y%m%d' }}" style="text-align:left;">{{ post.date | date: '%e&nbsp;%B' }}</h4>
        <ul>
        {% elsif month != nmonth %}
        </ul>
        </div>
      </div>
      <h3 class="split" id="{{ post.date | date: '%Y%m' }}" style="text-align:left;">{{ post.date | date: '%B&nbsp;%Y' }}</h3>
      <div class="monthfb">
      <div class="day">
      <h4 id="{{ post.date | date: '%Y%m%d' }}" style="text-align:left;">{{ post.date | date: '%e&nbsp;%B' }}</h4>
      <ul>
      {% elsif day != nday %}
    </ul>
    </div>
    <div class="day">
    <h4 id="{{ post.date | date: '%Y%m%d' }}" style="text-align:left;">{{ post.date | date: '%e&nbsp;%B' }}</h4>
    <ul>
    {% endif %}
    {% unless post.hidden == true %}
    <div style="display:flex; flex-wrap: wrap;"><li style="flex-grow:1; margin: auto 0 auto;"><a href="{{ site.baseurl }}{{ post.url }}">{{post.title | remove: " UTC Update"| date: "%H:%M" | replace: " ", "&nbsp;" }}</a></li>{% if post.published == false %}<div class="post-unpublished" style="margin:0;flex-grow:1"><p style="margin:1px 0 1px auto; width:min-content; text-align:end;">Unpublished</p></div>{% elsif post.hidden == true %}<div class="post-unpublished" style="margin:0;flex-grow:1"><p style="margin:1px 0 1px auto; width:min-content; text-align:end;">Hidden</p></div>{% endif %}</div>
    {% endunless %}
    {% endunless %}
    {% endfor %}
    </ul>
    </div>
    </div>
    </ul>
  </section>
</div>
