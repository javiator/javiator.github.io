---
name: create_evolution_post
description: Add a blog post to an existing evolutionary project.
---

# Create Evolution Post Skill

This skill creates a **complete, engaging blog post** for an evolutionary project using AI-assisted content generation. The agent writes the full post based on user context and guidance.

## Usage

**User Provides:**
- Post topic/title
- Context about what the post should cover
- Guidance on key points or learnings
- Pointers to code, repositories, or implementation details

**Agent Creates:**
- Complete, engaging blog post with all sections written
- Auto-generated frontmatter and Evolution Context
- Code examples, explanations, and insights
- Professional, well-structured content ready to publish

## Intelligent Workflow

### 1. Gather Context from User

**Ask user for:**
- **Post title/topic**: "What is the post about?"
- **Context**: "What should this post cover? Key points, code pointers, learnings?"

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

### 4. Generate Complete Post Content

**Using user's context and guidance, agent writes:**

#### Introduction Section
- Clear overview of what the post covers
- Why this topic matters in the evolution journey
- What readers will learn

#### Implementation Details Section
- Technical explanation of the work
- Code examples with syntax highlighting
- Architectural decisions and reasoning
- Integration points and patterns
- Mermaid diagrams where helpful (architecture, workflow, status)

#### Key Learnings Section
- Insights gained during implementation
- Challenges faced and solutions
- How this contributes to the evolution
- What to consider for future evolutions

**Agent researches:**
- Relevant code from repositories if provided
- Best practices for technologies mentioned
- Integration patterns for the stack
- Creates engaging, informative content

### 5. Apply Standard Includes

**Add navigation includes:**
```markdown
{% include evolution/evolution-posts.html %}
{% include evolution/post-navigation.html %}
```

### 6. Create Complete File

**Determine path:**
- Pattern: `_posts/YYYY/MM/YYYY-MM-DD-{project-slug}-{post-slug}.md`
- Generate slug from title (lowercase, hyphens)
- Create `_posts/YYYY/MM/` directory if needed

**Create file** with:
```markdown
---
{auto-generated frontmatter}
---

{auto-generated Evolution Context}

## Introduction

{AI-written introduction based on user context}

## Implementation Details

{AI-written technical content with code examples}

### {Subsection as needed}

{Detailed explanations, code snippets, diagrams}

## Key Learnings

{AI-written insights and takeaways}

{% include evolution/evolution-posts.html %}
{% include evolution/post-navigation.html %}
```

### 7. User Review

**Inform user:**
```
✅ Created complete evolution post: {filename}

Auto-generated:
  - Frontmatter with project/evolution metadata
  - Evolution Context linked to Evolution {N}
  - Categories: {categories}
  
AI-written content:
  - Introduction (contextualized for evolution)
  - Implementation Details (with code examples and explanations)
  - Key Learnings (insights and takeaways)

Ready for review and publishing!
```

## Example Interaction

```
USER: "Create evolution post about refactoring the API into separate modules"

AGENT: "Tell me about what you did - any code repos, key points, or learnings?"

USER: "Broke the monolithic Flask app into blueprints for auth, tenants, and users. 
Each module now has its own routes, models, and services. Code is at github.com/user/project.
Key learning was managing circular imports."

AGENT: "Which project?
  [1] Tenant Management
  [2] Smart Home Automation"

USER: "1"

AGENT: "Which evolution?
  [1] Evolution 1: Single-File Foundation
  [2] Evolution 2: Modular Architecture
  [3] Evolution 3: Java Enterprise Stack"

USER: "2"

AGENT: ✅ Created: _posts/2026/02/2026-02-10-tenant-management-api-modular-refactoring.md

Complete post written with:
  - Introduction explaining modular architecture benefits
  - Implementation section with:
    * Blueprint structure explanation
    * Code examples from your repo
    * Circular import solution details
    * Mermaid diagram showing module relationships
  - Key Learnings about separation of concerns

Categories: Architecture, Refactoring
Ready for review!
```

## Smart Features

1. **Content Generation**: AI writes complete, engaging post from user's context
2. **Code Integration**: Researches and includes relevant code examples
3. **Category Inference**: Keywords in title → categories from `_data/config.yml`
4. **Auto-Linking**: Previous evolution automatically linked in context
5. **Technical Depth**: Appropriate level of detail for the evolution stage
6. **Professional Quality**: Publication-ready content with proper structure

## Important Notes

- **Agent writes all content**, user provides guidance and context
- Post is **complete and ready to publish** after generation
- User can still edit/refine as needed
- Agent should ask follow-up questions if context is insufficient
- Include code examples, diagrams, and technical details
- Maintain consistent voice and learning journey narrative
