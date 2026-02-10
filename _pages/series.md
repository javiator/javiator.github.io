---
layout: single
title: "Content Series"
permalink: /series/
---

# Content Series

Explore curated collections of posts organized by topic and technology. Each series provides a focused learning path or deep dive into a specific subject.

---

{% for series_pair in site.data.series %}
  {% assign series_id = series_pair[0] %}
  {% assign series = series_pair[1] %}
  
  {% if series.status == "active" or series.status == "complete" %}
  ## {{ series.icon }} [{{ series.title }}](/series/{{ series_id }}/)
  
  {{ series.description }}
  
  {% assign series_posts = site.posts | where: "series", series_id %}
  **Posts**: {{ series_posts.size }} | **Status**: {{ series.status | capitalize }}
  
  [View Series →](/series/{{ series_id }}/)
  
  ---
  {% endif %}
{% endfor %}

## Start Your Journey

Use the links above to explore each series, or browse [all posts](/posts/) to discover content across all topics.
