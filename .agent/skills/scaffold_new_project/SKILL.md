---
name: scaffold_new_project
description: Initialize a new evolutionary project by creating data entries and directory structure.
---

# Scaffold New Project Skill

This skill sets up a new Evolutionary Project.

## Usage

Use this when starting a completely new project (e.g., "Smart Home Automation").

## Steps

1.  **Collect Project Info**:
    *   Project Name
    *   Project ID (slug)
    *   Description
    *   Initial Status (active)

2.  **Update `_data/projects.yml`**:
    *   Add new entry:
        ```yaml
        [project-id]:
          title: "[Project Name]"
          status: active
          description: "..."
          url: "/projects/[project-id]/"
        ```

3.  **Update `_data/evolutions.yml`**:
    *   Add new entry for Evolution 1:
        ```yaml
        [project-id]:
          - number: 1
            title: "[Evolution 1 Title]"
            status: active
            focus: "..."
            technologies: [...]
            url: "/projects/[project-id]/evolution-1/"
        ```

4.  **Create Directories**:
    *   `_pages/projects/[project-id]/`
    *   `_pages/projects/[project-id]/evolution-1/`
    *   `_pages/projects/[project-id]/posts/`

5.  **Create Index Pages**:
    *   `_pages/projects/[project-id]/index.md` (Project Hub):
        ```yaml
        ---
        layout: page
        title: [Project Title]
        permalink: /projects/[project-id]/
        project: [project-id]
        ---
        
        [Description]

        ## Evolution Timeline

        <div class="evolution-timeline">
          {% assign project_id = page.project %}
          {% assign evolutions = site.data.evolutions[project_id] | sort: "number" %}
          
          {% for evo in evolutions %}
          <div class="evolution-card {{ evo.status }}">
            <h3><a href="{{ evo.url }}">Evolution {{ evo.number }}: {{ evo.title }}</a></h3>
            <span class="status-badge {{ evo.status }}">{{ evo.status | capitalize }}</span>
            <p><strong>Focus:</strong> {{ evo.focus }}</p>
            <p><strong>Tech Stack:</strong> {{ evo.technologies | join: ", " }}</p>
          </div>
          {% endfor %}
        </div>
        ```
    *   `_pages/projects/[project-id]/evolution-1/index.md`:
        ```yaml
        ---
        layout: page
        title: "Evolution 1: [Evolution 1 Title]"
        permalink: /projects/[project-id]/evolution-1/
        project: [project-id]
        evolution_number: 1
        ---

        [Introduction/Context]

        {% include evolution/context.html %}

        ## Evolution Overview

        [Content]

        {% include evolution/navigation.html %}
        ```
    *   `_pages/projects/[project-id]/posts/index.md` (Project Timeline):
        ```yaml
        ---
        layout: page
        title: "All Posts: [Project Title]"
        permalink: /projects/[project-id]/posts/
        project: [project-id]
        ---

        This page shows all posts related to the [Project Title] project in chronological order.

        ## Chronological Post Timeline

        <div class="project-posts">
          {% assign project_posts = site.posts | where: "project", page.project | sort: "date" %}
          
          {% for post in project_posts reversed %}
          <div class="post-entry">
            <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
            <div class="meta">
                <span class="date">{{ post.date | date: "%B %d, %Y" }}</span> | 
                <span class="evolution">Evolution {{ post.evolution_number }}</span>
            </div>
            <p>{{ post.excerpt | strip_html | truncate: 160 }}</p>
          </div>
          {% endfor %}
        </div>
        ```

6.  **remind user**:
    *   Project structure is created. They can now use `create_evolution_post` to write the first post.
