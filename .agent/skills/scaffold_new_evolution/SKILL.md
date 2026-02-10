---
name: scaffold_new_evolution
description: Add a new evolution to an existing project.
---

# Scaffold New Evolution Skill

This skill adds a new evolution (e.g., Evolution 2) to an active project using templates from `_data/config.yml`.

## Usage

Use this when the user is ready to move to the next phase of a project.

## Steps

1.  **Collect Evolution Info**:
    *   Target Project (must exist in `_data/projects.yml`).
    *   Evolution Number.
    *   Title, Focus, Technologies.
    *   Status (active/planned).

2.  **Update `_data/evolutions.yml`**:
    *   Append new entry under the project key:
        ```yaml
        - number: [N]
          title: "[Title]"
          status: [active|planned]
          focus: "..."
          technologies: [...]
          url: "/projects/[project-id]/evolution-[N]/"
        ```

3.  **Create Directories**:
    *   Pattern from `_data/config.yml → file_paths.project_structure.evolution_page`
    *   `_pages/projects/[project-id]/evolution-[N]/`

4.  **Create Index Page**:
    *   Use templates from `_data/config.yml`
    *   Reference permalinks from `_data/config.yml → permalinks.evolution_page`
    *   `_pages/projects/[project-id]/evolution-[N]/index.md`:
        ```yaml
        ---
        layout: page
        title: "Evolution [N]: [Title]"
        permalink: /projects/[project-id]/evolution-[N]/
        project: [project-id]
        evolution_number: [N]
        ---

        [Introduction/Context]

        {% include evolution/context.html %}

        ## Evolution Overview

        [Content]

        {% include evolution/navigation.html %}
        ```

5.  **remind user**:
    *   Evolution page is created. They can now use `create_evolution_post` with the new evolution number.
