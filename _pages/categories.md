---
layout: page
permalink: /categories/
title: Categories
date: 2021-12-31
---


<div id="archives">
{% for category in site.categories %}
  {% assign posts = false %}
  <div class="archive-group">
    {% capture category_name %}{{ category | first }}{% endcapture %}
    <div id="#{{ category_name | slugize }}"></div>
    <p></p>
    <h3 style="text-transform: capitalize;" class="category-head">{% if category_name == "video" %}<a href="{{site.baseurl}}/categories/videos">{% elsif category_name == "live" %}<a href="{{site.baseurl}}/live">{% elsif category_name == "post" %}<a href="{{site.baseurl}}/posts">{% endif %}{{ category_name }}{% unless category_name == "live" %}s{% endunless %}{% if category_name == "video" or category_name == "live" or category_name == "post" %}</a>{% endif %}</h3>
    <a name="{{ category_name | slugize }}"></a>
    {% for post in site.categories[category_name] %}
    {% unless post.hidden == true %}
    <article class="archive-item">
      <p><center><b><a href="{{ site.baseurl }}{{ post.url }}">{% if post.title and post.title != "" %}{{post.title}}{% else %}{{post.excerpt |strip_html}}{%endif%}</a></b> - {% if post.date and post.date != "" %}{{ post.date | date: "%e %B %Y" }}{%endif%}</center></p>
    </article>
    {% assign posts = true %}
    {% endunless %}
    {% endfor %}
    {% if posts == false %}
    <p style="text-align:center;">This Category is Empty</p>
    {% endif %}
  </div>
{% endfor %}
</div>
