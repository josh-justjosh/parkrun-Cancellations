---
layout: default
permalink: /updates
---

[Back to the previous page](/more)
{% for post in site.posts %}
## {{ post.title }}
{{ post.content | markdownify }}
{% if forloop.first %}
<p style="text-align:right">You can subscribe to an RSS feed of these updates by using <a href="/feed.xml">this link</a>.</p>
{% endif %}
{% endfor %}