---
name: create_series
description: Create a new content series for grouping related posts by topic/technology.
---

# Create Series Skill

This skill initializes a new content series for non-evolutionary topic grouping (e.g., "Python Mastery", "AWS Journey").

## Usage

Use this when starting a new topic focus that will have multiple related posts NOT structured as evolutionary progressions.

## Workflow

### 1. Gather Series Information

**Ask for:**
- **Series name**: Human-readable title (e.g., "Python Mastery")
- **Series ID**: Slug for URLs (e.g., "python-mastery")
- **Description**: What the series covers
- **Icon**: Optional emoji icon (e.g., "🐍")
- **Tags**: Relevant tags (e.g., ["python", "programming", "backend"])

### 2. Add to Data Registry

**Append to `_data/series.yml`:**

```yaml
{series-id}:
  title: "{Series Name}"
  description: "{Description}"
  icon: "{Icon}"
  tags: [{tags}]
  status: "active"
```

### 3. Create Series Landing Page with AI-Generated Content

**Agent generates descriptive introduction** based on series details.

**Create `_pages/series/{series-id}/index.md`:**

```yaml
---
layout: page
title: "{Series Name}"
permalink: /series/{series-id}/
---

{icon} **{Series Name}**

{AI-written introduction explaining what this series covers, who it's for, and what readers will learn}

{{ site.data.series['{series-id}'].description }}

## Posts in this Series

{% assign series_posts = site.posts | where: "series", "{series-id}" | sort: "series_order" %}
{% if series_posts.size > 0 %}
{% for post in series_posts %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}
{% else %}
*No posts yet. Use `create_generic_post` to add posts to this series.*
{% endif %}

---

**Related Tags**: {% for tag in site.data.series['{series-id}'].tags %}#{{ tag }}{% unless forloop.last %}, {% endunless %}{% endfor %}
```

### 4. User Guidance

**Inform user:**
```
✅ Created series: {Series Name}

Series Details:
  - ID: {series-id}
  - Landing page: /series/{series-id}/
  - Status: active

Next steps:
  1. Use `create_generic_post` to add posts
  2. Set `series: "{series-id}"` in frontmatter
  3. Optionally set `series_order: N` for ordering

Example:
  "Create a generic post about Python decorators"
  → Select series: {Series Name}
  → Post automatically links to series
```

## Example

```
USER: "Create a series for Python content"

AGENT: "Series name?"
USER: "Python Mastery"

AGENT: "Series ID (slug)?"
USER: "python-mastery"

AGENT: "Description?"
USER: "Deep dives into Python concepts, patterns, and best practices"

AGENT: "Icon (emoji)?"
USER: "🐍"

AGENT: "Tags (comma-separated)?"
USER: "python, programming, backend"

AGENT: ✅ Created series: Python Mastery
  - Landing page: /series/python-mastery/
  - Use create_generic_post to add posts
  - Set series: "python-mastery" in frontmatter
```

##Configuration References

- Series registry: `_data/series.yml`
- Series landing page pattern: `_data/config.yml → file_paths.series_structure.series_hub`  - Permalink pattern: `_data/config.yml → permalinks.series_hub`
