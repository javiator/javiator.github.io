---
name: create_evolution_post
description: Add a blog post to an existing evolutionary project.
---

# Create Evolution Post Skill

This skill creates a blog post that is part of a larger Evolutionary Project, using intelligent automation to minimize user input.

## Usage

**Minimal User Input Required:**
- Post topic/title
- Project selection (from `_data/projects.yml`)
- Evolution selection (from `_data/evolutions.yml`)

**System Auto-Generates:**
- Frontmatter (from `_data/config.yml`)
- Evolution Context section (from `_data/evolutions.yml` + `_data/projects.yml`)
- Post structure (from `_data/config.yml`)
- Categories (inferred from keywords via `_data/config.yml`)
- File path and directory structure

## Intelligent Workflow

### 1. Gather Context

**Ask user for:**
- **Post title/topic**: "What is the post about?"

**Auto-detect project:**
- List available projects from `_data/projects.yml`
- Ask: "Which project? [1] {project1}  [2] {project2}..."
- User selects number

**Auto-detect evolution:**
- Load evolutions for selected project from `_data/evolutions.yml`
- Ask: "Which evolution? [1] Evolution 1: {title}  [2] Evolution 2: {title}..."
- User selects number

### 2. Auto-Generate Frontmatter

**Load template** from `_data/config.yml → templates.evolution_post.frontmatter`

**Populate fields:**
- `layout`: Use default from config (`post`)
- `title`: User-provided title
- `date`: Current date (YYYY-MM-DD)
- `project`: Project ID from selection
- `evolution_number`: Evolution number from selection
- `evolution`: "Evolution {N}: {title}" from `_data/evolutions.yml`
- `evolution_focus`: From `_data/evolutions.yml`
- `mermaid`: Default `true` from config
- `categories`: **Infer from title keywords** using `_data/config.yml → auto_population.categories_inference`
- `tags`: **Suggest from evolution focus** using `_data/config.yml → auto_population.tags_from_evolution_focus`

### 3. Auto-Generate Evolution Context

**Load template** from `_data/config.yml → auto_population.evolution_context_template`

**Populate placeholders:**
- `{evolution_number}`: From user selection
- `{evolution_title}`: From `_data/evolutions.yml[project][evolution_number].title`
- `{evolution_url}`: From `_data/evolutions.yml[project][evolution_number].url`
- `{project_title}`: From `_data/projects.yml[project].title`
- `{project_url}`: From `_data/projects.yml[project].url`
- `{evolution_focus}`: From `_data/evolutions.yml[project][evolution_number].focus`
- `{previous_evolution_context}`: 
  - If evolution_number > 1: "the {previous_evolution_title} established in [Evolution {N-1}]({previous_url})"
  - If evolution_number == 1: "the foundation phase"

**Result:**
```markdown
> **Evolution Context**: This post is part of [Evolution 2: Modular Architecture](/projects/tenant-management/evolution-2/) in the [Tenant Management: An Evolutionary Project](/projects/tenant-management/). This evolution focuses on Code organization and separation of concerns, building upon the Single-File Foundation established in [Evolution 1](/projects/tenant-management/evolution-1/).
```

### 4. Apply Standard Structure

**Load structure** from `_data/config.yml → templates.evolution_post.structure`

**Create file with:**
```markdown
---
{auto-generated frontmatter}
---

{auto-generated Evolution Context}

## Introduction

[User writes introduction here]

## Implementation Details

[User writes implementation here]

## Key Learnings

[User writes key learnings here]

{% include evolution/evolution-posts.html %}
{% include evolution/post-navigation.html %}
```

### 5. Create File

**Determine path:**
- Pattern: `_posts/YYYY/MM/YYYY-MM-DD-{project-slug}-{post-slug}.md`
- Generate slug from title (lowercase, hyphens)
- Create `_posts/YYYY/MM/` directory if needed

**Create file** at calculated path with pre-populated content

### 6. User Guidance

**Inform user:**
```
✅ Created evolution post: {filename}

Auto-populated:
  - Frontmatter with project/evolution metadata
  - Evolution Context linked to Evolution {N}
  - Standard structure with sections
  - Inferred categories: {categories}
  
Ready for content:
  - Introduction section
  - Implementation Details section
  - Key Learnings section
```

## Example Interaction

```
USER: "Create evolution post about API refactoring"

AGENT: "Which project? 
  [1] Tenant Management
  [2] Smart Home Automation"

USER: "1"

AGENT: "Which evolution?
  [1] Evolution 1: Single-File Foundation
  [2] Evolution 2: Modular Architecture
  [3] Evolution 3: Java Enterprise Stack"

USER: "2"

AGENT: ✅ Created: _posts/2026/02/2026-02-10-tenant-management-api-refactoring.md

Auto-populated:
  - Project: tenant-management
  - Evolution: 2 (Modular Architecture)
  - Categories: Architecture, Refactoring (inferred from keywords)
  - Evolution Context: Linked to Evolution 2, references Evolution 1
  - Structure: Introduction, Implementation, Key Learnings sections ready

File is ready for your content!
```

## Smart Features

1. **Category Inference**: Keywords in title → categories from `_data/config.yml`
2. **Auto-Linking**: Previous evolution automatically linked in context
3. **Date Management**: Current date auto-applied
4. **Path Generation**: File path calculated from date + project + title
5. **Structure Pre-Population**: Standard sections already in place

