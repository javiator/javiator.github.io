---
name: create_evolution_post
description: Add a blog post to an existing evolutionary project.
---

# Create Evolution Post Skill

This skill creates a blog post that is part of a larger Evolutionary Project, using the centralized `_data` configuration.

## Usage

Use this when the user wants to add a post (e.g., "Refactoring API") to an active project (e.g., "Tenant Management", Evolution 3).

## Steps

1.  **Identify Project and Evolution**:
    *   Ask user for the Project Name or ID (must match a key in `_data/projects.yml`).
    *   Ask user for the Evolution Number (must exist in `_data/evolutions.yml`).

2.  **Determine Date and Title**:
    *   Generate slug from title.
    *   Target Path: `_posts/YYYY/MM/YYYY-MM-DD-project-slug-post-slug.md`

3.  **Create File**:
    Ensure `_posts/YYYY/MM/` exists.

4.  **Frontmatter Template**:
    ```yaml
    ---
    layout: post
    title: "[Title]"
    date: YYYY-MM-DD
    categories: [Recommended Categories]
    tags: [Recommended Tags]
    project: "[Project ID (e.g. tenant-management)]"
    evolution_number: [Number]
    # 'evolution' and 'evolution_focus' are no longer strictly required in frontmatter 
    # if the includes use site.data.evolutions, BUT keeping them is good for redundancy 
    # or if includes still rely on page variables. 
    # Let's include them for backward compatibility or clarity.
    evolution: "Evolution [N]: [Title from _data]"
    evolution_focus: "[Focus from _data]"
    mermaid: true
    ---

    > **Evolution Context**: This post is part of [Evolution [N]: [Title from _data]]([URL from _data]) in the [[Project Title] from _data]([Project URL] from _data). This evolution focuses on [Focus from _data], building upon the [Previous Foundation/Evolution] established in [[Previous Evolution Link]].

    Introduction...

    ## Heading

    Content...

    {% include evolution/evolution-posts.html %}
    {% include evolution/post-navigation.html %}
    ```

5.  **remind user**:
    *   This post will automatically appear in the implementation lists due to the new data-driven includes, *provided* the frontmatter has the correct `project` and `evolution_number`.
