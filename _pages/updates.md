---
layout: page
permalink: /updates
title: 'parkrun Cancellation Updates'
---

[Back to the 'more info' page](/more)
<div class="posts">
{% for post in site.posts %}
<article class="post">
<a href="{{ post.url }}"><h2>{{ post.title }}</h2></a>
<div class='hscrollable'>
{{ post.content | markdownify }}
</div>
</article>
{% if forloop.first %}
<div style="padding-bottom: 0" class="post">
<p>You can subscribe to an RSS feed of these updates by using <a href="/feed.xml">this link</a> or you can use these IFTTT applets to send you <a href="https://ifttt.com/applets/bbtnkTzV-email-parkrun-cancellations-updates">an email</a> or <a href="https://ifttt.com/applets/nCmTgRLc-parkrun-cancellations-notifier">a notification</a> when there's an update.</p>
</div>
{% endif %}
{% endfor %}
</div>
