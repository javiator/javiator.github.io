# AI Agent Skills Guide

This guide documents the available skills for managing Javiator's Blog project derived from the `implementation_plan.md` and `HOW_TO_PROMPTS.md`.

## Content Creation Skills

> **Note on Folder Structure**:
> - Existing posts remain in `_posts/` to preserve historical URLs.
> - *New* posts created by these skills are automatically organized into `_posts/YYYY/MM/`.
> - This hybrid approach ensures backward compatibility while improving future organization.

### 1. `create_generic_post`
**Purpose**: Create independent blog posts not associated with any "Evolutionary Project".
**Use Case**: Writing about a new tool, a general concept, or a personal update.
**Input**:
*   `Title`: The post title.
*   `Date`: YYYY-MM-DD.
*   `Categories/Tags`.
**Output**:
*   Creates `_posts/YYYY/MM/YYYY-MM-DD-slug.md`.
**Side Effects**: None.

### 2. `create_evolution_post`
**Purpose**: Add a new post to an **existing** Evolutionary Project.
**Use Case**: Documenting progress on "Tenant Management" (e.g., "Adding Spring Security").
**Input**:
*   `Project ID`: (e.g., `tenant-management`).
*   `Evolution Number`: (e.g., `3`).
*   `Title`, `Date`, etc.
**Output**:
*   Creates `_posts/YYYY/MM/YYYY-MM-DD-slug.md`.
*   Includes `project` and `evolution_number` metadata.
*   Uses `{% include evolution/context.html %}` for dynamic project context.
*   Uses `{% include evolution/evolution-posts.html %}` and `{% include evolution/post-navigation.html %}` for navigation.

**Template Structure**:
```yaml
---
layout: post
title: "..."
project: [id]
evolution_number: [N]
---

[Content...]

{% include evolution/evolution-posts.html %}
{% include evolution/post-navigation.html %}
```

## Project Management Skills

### 3. `scaffold_new_project`
**Purpose**: Initialize a completely new Evolutionary Project.
**Use Case**: Starting a new series (e.g., "Smart Home Automation").
**Input**:
*   `Project Name`, `ID`, `Description`.
**Output**:
*   Adds entry to `_data/projects.yml`.
*   Adds initial entry to `_data/evolutions.yml`.
*   Creates `_pages/projects/[id]/index.md` (Project Hub) with dynamic evolution timeline.
*   Creates `_pages/projects/[id]/evolution-1/index.md` with dynamic context and navigation.
*   Creates `_pages/projects/[id]/posts/index.md` with dynamic post list.
**Side Effects**: Project becomes visible in the "All Projects" list and has a landing page.

### 4. `scaffold_new_evolution`
**Purpose**: Start a new phase for an existing project.
**Use Case**: Moving from "Evolution 1" to "Evolution 2".
**Input**:
*   `Project ID`.
*   `Evolution Number`.
*   `Title`, `Focus`, `Technologies`.
**Output**:
*   Appends entry to `_data/evolutions.yml`.
*   Creates `_pages/projects/[id]/evolution-[N]/index.md` pre-configured with:
    *   `{% include evolution/context.html %}`
    *   `{% include evolution/navigation.html %}`
**Side Effects**: New evolution appears in the project timeline and navigation.
