# AI Agent Skills Guide

This guide documents the available skills for managing Javiator's Blog project with intelligent automation and centralized configuration.

## Architecture Overview

### Data-Driven System

All skills leverage centralized data sources:
- **`_data/projects.yml`**: Project registry
- **`_data/evolutions.yml`**: Evolution metadata
- **`_data/config.yml`**: Templates, standards, and automation rules

### Automation-First Design

Skills minimize user input and auto-generate:
- Frontmatter with metadata
- Evolution Context sections
- Post structure and sections
- Categories (inferred from keywords)
- File paths and directory structure

---

## Content Creation Skills

> **Note on Folder Structure**:
> - Existing posts remain in `_posts/` to preserve historical URLs.
> - *New* posts created by these skills are automatically organized into `_posts/YYYY/MM/`.
> - This hybrid approach ensures backward compatibility while improving future organization.

### 1. `create_evolution_post` (Intelligent Automation)

**Purpose**: Create evolution posts with minimal user input.

**User Provides:**
- Post topic/title
- Project selection (from interactive list)
- Evolution selection (from interactive list)

**System Auto-Generates:**
- Complete frontmatter (from `_data/config.yml`)
- Evolution Context (from `_data/evolutions.yml` + `_data/projects.yml`)
- Standard structure with sections
- Categories (inferred from title keywords)
- File path: `_posts/YYYY/MM/YYYY-MM-DD-{project-slug}-{post-slug}.md`

**Smart Features:**
1. **Category Inference**: Keywords in title → categories via `_data/config.yml`
2. **Auto-Linking**: Previous evolution automatically linked in context
3. **Date Management**: Current date auto-applied
4. **Structure Pre-Population**: Introduction, Implementation, Key Learnings sections ready

**Configuration Reference:**
- Template: `_data/config.yml → templates.evolution_post`
- Auto-population: `_data/config.yml → auto_population`

---

### 2. `create_generic_post` (Enhanced with Post Types)

**Purpose**: Create standalone blog posts with intelligent post type detection.

**Post Types Available:**
1. **Tutorial** - Step-by-step guides
2. **Deep Dive** - Technical analysis and exploration  
3. **Tool Review** - Tool evaluation and comparison
4. **Quick Tip** - Short productivity enhancers
5. **Concept Explanation** - Fundamental concept breakdowns
6. **Other** - General posts

**User Provides:**
- Post type selection
- Title/topic
- Series association (optional)

**System Auto-Generates:**
- Categories based on post type
- Structure template for post type
- Series metadata (if applicable)
- File path: `_posts/YYYY/MM/YYYY-MM-DD-{post-slug}.md`

**Example: Tutorial Post**
```
USER: "What type? [1] Tutorial"
SYSTEM: Auto-suggests categories: [Tutorial, Learning]
SYSTEM: Structure: Intro, Prerequisites, Step-by-Step, Conclusion
```

**Configuration Reference:**
- Post types: `_data/config.yml → templates.generic_post.post_types`
- Series list: `_data/series.yml`

---

## Content Series Management

### 3. `create_series`

**Purpose**: Create a new content series for grouping related posts by topic/technology.

**Use Case**: Starting a topic focus like "Python Mastery", "AWS Journey", or "React Patterns".

**User Provides:**
- Series name
- Series ID (slug)
- Description
- Icon (optional emoji)
- Tags

**System Creates:**
1. Entry in `_data/series.yml`
2. Landing page: `_pages/series/{series-id}/index.md`

**Example:**
```
USER: "Create series for Python content"
SYSTEM: Creates "Python Mastery" series
RESULT:
  - Landing page: /series/python-mastery/
  - Use with create_generic_post
  - Set series: "python-m
```

**Result:** Series ready for posts via `create_generic_post`.

---

## Project Management Skills

### 4. `scaffold_new_project`

**Purpose**: Initialize a completely new evolutionary project.

**Use Case**: Starting a new learning series (e.g., "Smart Home Automation", "E-Commerce Platform").

**User Provides:**
- Project name
- Project ID (slug)
- Description
- Evolution 1 details (title, focus, technologies)

**System Creates:**
1. **Data Entries:**
   - Entry in `_data/projects.yml`
   - Initial entry in `_data/evolutions.yml`

2. **Directory Structure** (from `_data/config.yml → file_paths.project_structure`):
   - `_pages/projects/{project-id}/`
   - `_pages/projects/{project-id}/evolution-1/`
   - `_pages/projects/{project-id}/posts/`

3. **Pages** (using `_data/config.yml` templates):
   - `_pages/projects/{project-id}/index.md` (Project Hub with dynamic evolution timeline)
   - `_pages/projects/{project-id}/evolution-1/index.md` (Evolution 1 page)
   - `_pages/projects/{project-id}/posts/index.md` (Chronological post timeline)

**Result:** Project is immediately visible and ready for content creation via `create_evolution_post`.

---

### 5. `scaffold_new_evolution`

**Purpose**: Add a new evolution to an existing project.

**Use Case**: Transitioning from "Evolution 2" to "Evolution 3".

**User Provides:**
- Project ID
- Evolution number
- Title, focus, technologies
- Status (active/planned)

**System Creates:**
1. **Data Entry:**
   - Appends entry to `_data/evolutions.yml` under project key

2. **Directory** (from `_data/config.yml → file_paths.project_structure`):
   - `_pages/projects/{project-id}/evolution-{N}/`

3. **Page** (using `_data/config.yml` templates):
   - `_pages/projects/{project-id}/evolution-{N}/index.md`
   - Pre-configured with:
     - `{% include evolution/context.html %}`
     - `{% include evolution/navigation.html %}`

**Result:** New evolution appears in project timeline and navigation. Ready for posts via `create_evolution_post`.

---

## Configuration System

All skills reference `_data/config.yml` for:
- **Post Templates**: Frontmatter structure and content sections
- **Auto-Population Rules**: Evolution Context templates, category inference
- **File Paths**: Directory patterns and naming conventions
- **Standards**: Mermaid colors, quality checklists, content guidelines

See `_data/config.yml` for complete configuration documentation.

---

## Workflow Examples

### Creating First Post for New Project

1. `scaffold_new_project` → Initialize "Smart Home Automation"
2. `create_evolution_post` → Add first post to Evolution 1
3. System auto-populates everything from centralized config

### Adding Evolution to Existing Project

1. `scaffold_new_evolution` → Add Evolution 4 to "Tenant Management"
2. `create_evolution_post` → Create posts for Evolution 4
3. Evolution Context automatically links to Evolution 3

### Standalone Content

### Creating Content for New Series

1. `create_series` → Initialize "Python Mastery"
2. `create_generic_post` → Tutorial about decorators (type: Tutorial, series: python-mastery)
3. `create_generic_post` → Deep dive into metaclasses (type: Deep Dive, series: python-m
4. Series landing page auto-lists all posts

### Creating Evolution Content

1. `scaffold_new_project` → "Smart Home" project
2. `create_evolution_post` → First post in Evolution 1
3. Evolution Context automatically generated

### Creating Standalone Content

1. `create_generic_post` → Quick tip about VSCode shortcut
2. Select type: Quick Tip
3. No series association
4. Appears in main blog feed

---

*For detailed implementation, see `.cursor/rules/` and `_data/config.yml`.*
