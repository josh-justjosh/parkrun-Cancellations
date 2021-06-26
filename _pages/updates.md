---
layout: page
permalink: /updates
title: 'parkrun Cancellation Updates'
---

[Back to the 'more info' page](/more)
{% for post in site.posts %}
## {{ post.title }}
{{ post.content | markdownify }}
{% if forloop.first %}
You can subscribe to an RSS feed of these updates by using [this link](/feed.xml) or you can use these IFTTT applets to send you [an email](https://ifttt.com/applets/bbtnkTzV-email-parkrun-cancellations-updates) or [a notification](https://ifttt.com/applets/nCmTgRLc-parkrun-cancellations-notifier) when there's an update.
{% endif %}
{% endfor %}