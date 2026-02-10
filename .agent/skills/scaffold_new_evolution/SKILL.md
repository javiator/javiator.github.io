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

4.  **Create Index Page with AI-Generated Content**:
    *   Use templates from `_data/config.yml`
    *   Reference permalinks from `_data/config.yml → permalinks.evolution_page`
    *   **Agent generates descriptive content** based on evolution details
    
    *   `_pages/projects/[project-id]/evolution-[N]/index.md`:
        ```yaml
        ---
        layout: page
        title: "Evolution [N]: [Title]"
        permalink: /projects/[project-id]/evolution-[N]/
        project: [project-id]
        evolution_number: [N]
        ---

        {AI-written introduction explaining this evolution's goals, focus, and how it builds on previous work}

        {% include evolution/context.html %}

        ## Evolution Overview

        {AI-written overview covering:
         - What this evolution addresses
         - Key technologies and patterns being used
         - How it advances from previous evolution
         - What readers can expect from posts in this evolution
        }

        {% include evolution/navigation.html %}
        ```

5.  **Inform User**:
    ```
    ✅ Created Evolution [N]: [Title]
    
    Evolution Details:
      - Project: [Project Title]
      - Focus: [Focus area]
      - Technologies: [Tech stack]
      - Page: /projects/[project-id]/evolution-[N]/
    
    AI-generated content:
      - Evolution introduction
      - Overview of goals and approach
    
    Next steps:
      - Use create_evolution_post to write posts for this evolution
      - Posts will automatically link to this evolution page
    ```
