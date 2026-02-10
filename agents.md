# AI Agent Guidelines for Javiator's Blog

This document provides a high-level overview for AI agents working with this blog project. For detailed implementation guidelines, refer to the Cursor rules in `.cursor/rules/` and the centralized configuration in `_data/config.yml`.

## Project Overview

This is a Jekyll-based blog showcasing **systematic learning through evolutionary projects** - taking domains and evolving them through multiple architectural approaches, technology stacks, and complexity levels.

Each project is a **portfolio-quality case study** demonstrating progressive complexity, technology mastery, and real-world application development.

## Architecture (Multi-Project Ready)

### Data-Driven System

All project and evolution metadata is centralized in `_data/`:

- **`_data/projects.yml`**: Registry of all evolutionary projects
- **`_data/evolutions.yml`**: Evolution metadata for all projects (keyed by project ID)
- **`_data/series.yml`**: Content series registry for topic-based grouping
- **`_data/config.yml`**: Universal templates, standards, patterns, and automation rules

### Cursor Rules Structure

Modern Cursor rules format in `.cursor/rules/` directory:

- **`evolutionary-project-framework.mdc`**: Universal philosophy and multi-project framework
- **`content-creation.mdc`**: Content creation guidelines and automation features
- **`technical-standards.mdc`**: Technical standards and implementation details
- **`information-freshness.mdc`**: Information currency and verification standards

### Skills Architecture

AI skills in `.agent/skills/` provide intelligent automation:

- **`create_evolution_post`**: Automated post creation with minimal user input
- **`create_generic_post`**: Generic post creation with post type detection
- **`create_series`**: Initialize content series for topic grouping
- **`scaffold_new_project`**: Initialize new evolutionary projects
- **`scaffold_new_evolution`**: Add new evolutions to existing projects

See [SKILLS_GUIDE.md](SKILLS_GUIDE.md) for detailed skill documentation.

## Core Principles (Universal)

1. **Progressive Complexity**: Each evolution builds upon previous learnings
2. **Technology Mastery**: Deep dive into different technology stacks
3. **Architectural Patterns**: From simple to enterprise-ready architectures
4. **Decision Documentation**: Explain reasoning behind each architectural choice
5. **Portfolio Value**: Comprehensive case studies in software evolution

## Quick Reference

### Current Projects

See `_data/projects.yml` for the current list of active evolutionary projects.

**Example: Tenant Management Project**
- Evolution 1: Single-File Foundation (Complete)
- Evolution 2: Modular Architecture (Complete)
- Evolution 3: Java Enterprise Stack (Complete)
- Evolution 4: AI Integration Layer (Complete)
- Evolution 5: Conversational Interface (Complete)
- Evolution 6: Cloud Deployment Strategies (Complete)

### Content Creation Workflow

#### For Evolution Posts (Automated)

Use the `create_evolution_post` skill:

1. **User provides**: Topic/title
2. **System prompts**: Which project? Which evolution?
3. **System auto-generates**:
   - Frontmatter with all metadata
   - Evolution Context section
   - Standard structure with sections
   - File path and location
   - Categories (inferred from keywords)

**Example:**
```
USER: "Create evolution post about API refactoring"
SYSTEM: Lists projects → User selects
SYSTEM: Lists evolutions → User selects
SYSTEM: ✅ Creates fully populated post ready for content
```

## AI Content Generation Philosophy

**All skills generate complete, publication-ready content:**

- **Agent writes full content**, not skeletons with placeholders
- **User provides**: Context, guidance, key points, code pointers
- **Agent creates**: Complete articles, descriptions, overviews
- Applies to: Blog posts, project pages, evolution pages, series pages
- User reviews/edits if desired, but content is publication-ready

**Example:**
```
USER: "Create evolution post - I refactored the API into modules"
AGENT: "Tell me more - what did you do?"
USER: "Split Flask into blueprints, here's the repo link, key learning was circular imports"
AGENT: [Creates complete post with intro, implementation details with code examples, learnings]
USER: [Reviews and publishes]
```

#### For Generic Posts (Enhanced)

Use the `create_generic_post` skill for standalone content with intelligent post type detection.

**Post Types Available:**
1. **Tutorial** - Step-by-step guides
2. **Deep Dive** - Technical analysis
3. **Tool Review** - Tool evaluations
4. **Quick Tip** - Productivity enhancers
5. **Concept Explanation** - Fundamental breakdowns

**Workflow:**
1. **User selects**: Post type
2. **User provides**: Title/topic
3. **User chooses**: Part of series? (optional)
4. **System auto-generates**:
   - Categories based on post type
   - Structure template for type
   - Series metadata (if applicable)

**Example:**
```
USER: "Create generic post about Python decorators"
SYSTEM: "What type? [1] Tutorial [2] Deep Dive..."
USER: "1" (Tutorial)
SYSTEM: "Part of series? [1] Python Mastery [2] No"
USER: "1"
SYSTEM: ✅ Creates tutorial with Python Mastery series link
```

## Content Organization

The blog supports three content organization patterns:

### 1. Evolutionary Projects
- **Structure**: Sequential evolutions building upon each other
- **Example**: Tenant Management (Evolution 1 → 2 → 3...)
- **Use when**: Building comprehensive architectural case studies
- **Skills**: `create_evolution_post`, `scaffold_new_project`, `scaffold_new_evolution`

### 2. Content Series
- **Structure**: Topic-focused collections, non-sequential
- **Example**: "Python Mastery", "AWS Journey", "React Patterns"
- **Use when**: Exploring a technology or concept with related posts
- **Skills**: `create_series`, `create_generic_post` (with series)
- **Registry**: `_data/series.yml`
- **Landing pages**: Auto-generated at `/series/{series-id}/`

### 3. Standalone Posts
- **Structure**: Individual, unrelated posts
- **Example**: Quick tips, tool reviews, concept explanations
- **Use when**: Sharing specific insights not part of larger collection
- **Skills**: `create_generic_post` (no series)

## Essential Post Requirements

### Evolution Posts MUST Include

- **Evolution Context**: Auto-generated from `_data/evolutions.yml` and `_data/projects.yml`
- **Evolution Metadata**: `project`, `evolution_number` in frontmatter
- **Navigation Includes**: 
  - `{% include evolution/post-navigation.html %}`
  - `{% include evolution/evolution-posts.html %}`

### All Posts Should Include

- Clear, descriptive title
- Proper categorization (see `_data/config.yml`)
- Code examples with syntax highlighting
- Key learnings or conclusion section

## Intelligent Automation Features

The system provides:

1. **Category Inference**: Keywords in title → categories from `_data/config.yml`
2. **Auto-Linking**: Previous evolution automatically linked in Evolution Context
3. **Date Management**: Current date auto-applied
4. **Path Generation**: File path calculated from date + project + title
5. **Structure Pre-Population**: Standard sections ready for content

## Success Criteria

### For New Content
- ✅ Properly assigned to project and evolution
- ✅ Includes evolution metadata (for evolution posts)
- ✅ Has appropriate navigation links
- ✅ Uses Mermaid diagrams where relevant
- ✅ Maintains learning journey narrative

### For Updates
- ✅ Preserves evolution context
- ✅ Updates navigation components
- ✅ Keeps diagrams current
- ✅ Maintains systematic progression

## Adding New Projects

Use the `scaffold_new_project` skill to:
1. Add project entry to `_data/projects.yml`
2. Create first evolution in `_data/evolutions.yml`
3. Generate directory structure
4. Create project hub and evolution pages

## Detailed Guidelines

For comprehensive implementation details:
- **Framework**: `.cursor/rules/evolutionary-project-framework.mdc`
- **Content Creation**: `.cursor/rules/content-creation.mdc`
- **Technical Standards**: `.cursor/rules/technical-standards.mdc`
- **Universal Config**: `_data/config.yml`
- **Skills Guide**: `SKILLS_GUIDE.md`

---

*This framework represents a learning-first, multi-project approach to software development, where each evolution serves both practical and educational purposes.*