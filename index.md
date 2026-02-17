---
title: "Welcome to My Learning Journey!"
permalink: /
layout: single
author_profile: true
title: false
related: true
toc: true
toc_label: "Table of Contents"
toc_sticky: true
toc_sidebar: true
sidebar:
header:
  overlay_image: /assets/images/headers/welcome-learning-journey.png
  overlay_filter: 0.5
---

**Welcome to my corner of the internet** where I share my journey of learning and growing in the world of technology and solution architecture.

## What This Blog Is About

| **Content Type** | **What You'll Find** |
|------------------|---------------------|
| **What This Blog Is About** | • Things I'm exploring in architecture and solution design<br>• Projects I'm working on and what I learn from them<br>• Mistakes I make (because that's how we learn!)<br>• Interesting technologies and patterns I discover |
| **Learning Adventures** | • My experiments with different architectural patterns<br>• Step-by-step walkthroughs of things I'm trying<br>• "What I learned this week" type posts<br>• Simple explanations of complex concepts |
| **Project Stories** | • Updates on my [GitHub projects](https://github.com/javiator) and what I'm building<br>• Behind-the-scenes of how I approach problems<br>• What worked, what didn't, and why<br>• Code snippets and examples |
| **Sharing Knowledge** | • Interesting articles and resources I find<br>• Tools and techniques that make my work easier<br>• Lessons from working with different technologies<br>• Tips I pick up from the community |

## Featured Project: Tenant Management Evolution

**An Evolutionary Journey Through Architecture**

Follow my systematic approach to evolving a single project through 6 different architectural approaches, from single-file to cloud-deployed AI-enhanced applications.

**Current Evolution**: Evolution 6 - Cloud Deployment Strategies (Complete) ✅  
**Total Posts**: 11 posts across 6 evolutions  
**Technologies**: Python, Flask, Java, Spring Boot, React, Docker, MCP, LLM APIs, NLP, AWS, Terraform

[Explore the Evolution →](/projects/tenant-management/)

## Featured Posts

{% assign featured_posts = site.posts | where: "featured", true %}
{% for post in featured_posts limit:2 %}

>  [**{{ post.title }}**]({{ post.url }})<br>
*{{ post.date | date: "%B %d, %Y" }} • {{ post.categories | join: ", " }} • {{ post.content | number_of_words | divided_by: 200 | plus: 1 }} min read*<br><br>{{ post.excerpt | strip_html | truncate: 150 }}<br><br>[Continue reading →]({{ post.url }}) 

{% endfor %}

## Standalone Articles

Independent technical articles covering various topics, not tied to specific projects.

{% assign standalone_posts = site.posts | where_exp: "post", "post.project == nil" | sort: "date" | reverse %}
{% for post in standalone_posts limit:3 %}
| [**{{ post.title }}**]({{ post.url }})<br><br>*{{ post.date | date: "%B %d, %Y" }} • {{ post.categories | join: ", " }} • {{ post.content | number_of_words | divided_by: 200 | plus: 1 }} min read*<br><br>{{ post.excerpt | strip_html | truncate: 120 }}<br><br>[Read more →]({{ post.url }}) |

{% endfor %}

[View All Standalone Articles →](/posts/#standalone) • [View All Posts →](/posts/)

## Recent Posts

{% assign recent_posts = site.posts | where_exp: "post", "post.featured != true" %}
{% for post in recent_posts limit:3 %}
| [**{{ post.title }}**]({{ post.url }})<br><br>*{{ post.date | date: "%B %d, %Y" }} • {{ post.categories | join: ", " }} • {{ post.content | number_of_words | divided_by: 200 | plus: 1 }} min read*<br><br>{{ post.excerpt | strip_html | truncate: 120 }}<br><br>[Read more →]({{ post.url }}) |

{% endfor %}

[View All Posts →](/posts/)

## Content Overview

**{{ site.posts.size }} Posts** covering **{{ site.categories.size }} Topics** • **{{ site.tags.size }} Tags** for easy discovery

{% assign standalone_count = site.posts | where_exp: "post", "post.project == nil" | size %}
{% assign project_count = site.posts | where_exp: "post", "post.project != nil" | size %}

**Content Breakdown:** {{ standalone_count }} Standalone Articles • {{ project_count }} Project Posts  
**Popular Topics:** Architecture, Development, Requirements Analysis, AI Integration  
**Content Types:** Tutorials, Case Studies, Learning Notes, Project Walkthroughs, Strategy Guides

## Explore by Topic

| **Topic** | **Description** | **Explore** |
|-----------|-----------------|-------------|
| **Architecture** | System design & patterns | [Explore →](/categories/#architecture) |
| **Development** | Full-stack tutorials | [Explore →](/categories/#development) |
| **AI Integration** | AI adoption & strategy | [Explore →](/categories/#ai-integration) |
| **Requirements** | Analysis & planning | [Explore →](/categories/#requirements) |
| **Standalone Articles** | Independent technical content | [View All →](/posts/#standalone) |


## Stay Updated

Want to follow my learning journey? Connect with me and stay updated on new content.

- **[GitHub](https://github.com/javiator)** - View my projects and code contributions
- **[LinkedIn](https://www.linkedin.com/in/amans82/)** - Connect for professional discussions


Thanks for joining me on this learning adventure!

*P.S. – This is a journey, not a destination. Let's learn and grow together!*
