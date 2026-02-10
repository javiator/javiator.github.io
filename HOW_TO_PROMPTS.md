# How to Prompts: Blog Post Creation Guide

This guide provides standardized prompts for creating different types of blog posts in the Javiator's Blog system. Use these prompts when working with AI agents to ensure consistent post creation and proper project structure updates.

## Table of Contents

1. [Generic Post (Not Part of Any Project)](#1-generic-post-not-part-of-any-project)
2. [New Post for New Project with Evolution Set](#2-new-post-for-new-project-with-evolution-set)
3. [New Post for Existing Evolution](#3-new-post-for-existing-evolution)

---
See [SKILLS_GUIDE.md](SKILLS_GUIDE.md) for detailed skill usage.

## 1. Generic Post (Not Part of Any Project)

Use this prompt when creating a standalone blog post that is not part of any evolutionary project.

```
Create a new blog post with the following requirements:

**Post Details:**
- Title: [Your Title Here]
- Date: [Current Date]
- Categories: [Relevant Categories]
- Tags: [Relevant Tags]
- Content Type: [content-type]
- Learning Focus: [learning-focus-array]
- Difficulty: [beginner/intermediate/advanced]

**Content Requirements:**
- Write engaging, informative content
- Include proper headings and structure
- Add code examples if relevant
- Include a conclusion section

**Post Structure:**
- Introduction paragraph
- Main content with proper headings
- Code examples (if applicable)
- Key takeaways section
- Conclusion

**File Location:**
- Create in `_posts/` directory with proper naming convention: `YYYY-MM-DD-post-title.md`

**Important Notes:**
- This is a standalone post, NOT part of any evolutionary project
- Do NOT add any evolution metadata
- Do NOT include evolution context or navigation components
- Keep it focused on the specific topic without project references
```

---

## 2. New Post for New Project with Evolution Set

Use this prompt when creating the first post of a new evolutionary project.

```
Create a new blog post for a NEW evolutionary project with the following requirements:

**Post Details:**
- Title: [Your Title Here]
- Date: [Current Date]
- Categories: [Relevant Categories]
- Tags: [Relevant Tags]
- Content Type: [content-type]
- Learning Focus: [learning-focus-array]
- Difficulty: [beginner/intermediate/advanced]

**Evolutionary Project Fields:**
- project: "[Project Name]"
- project_type: "evolutionary"
- evolution: "Evolution 1: [Evolution Name]"
- evolution_number: 1
- evolution_focus: "[Focus Area]"

**Content Requirements:**
- Write engaging, informative content
- Include evolution context at the beginning
- Add proper headings and structure
- Include code examples if relevant
- Add evolution navigation components

**Post Structure:**
- Introduction paragraph
- Evolution context block (using include)
- Main content with proper headings
- Code examples (if applicable)
- Key takeaways section
- Evolution posts component
- Post navigation component
- Conclusion

**Required Updates:**
1. **Create Project Structure:**
   - Create `_pages/projects/[project-name]/index.md` (main project hub)
   - Create `_pages/projects/[project-name]/evolution-1/index.md` (first evolution page)
   - Create `_pages/projects/[project-name]/posts/index.md` (posts timeline)
   - Create `_pages/projects/[project-name]/evolution-2/index.md` through `evolution-5/index.md` (planned evolutions)

2. **Update Homepage:**
   - Add new project to featured projects section in `index.md`
   - Include project description, current evolution, and link

3. **Update Projects Page:**
   - Add new project to the projects list in `_pages/projects.md`
   - Include project description and link

4. **Create Evolution Pages:**
   - Each evolution page should include goals, posts, and navigation
   - Mark appropriate evolutions as complete/active/planned

5. **Update Navigation:**
   - Ensure project is accessible from main navigation

**File Location:**
- Create in `_posts/` directory with proper naming convention: `YYYY-MM-DD-post-title.md`

**Include Components:**
- Add `{% include evolution/post-navigation.html %}` at the end
- Add `{% include evolution/evolution-posts.html %}` before post navigation
```

---

## 3. New Post for Existing Evolution

Use this prompt when creating a new post for an existing evolutionary project.

```
Create a new blog post for an EXISTING evolutionary project with the following requirements:

**Post Details:**
- Title: [Your Title Here]
- Date: [Current Date]
- Categories: [Relevant Categories]
- Tags: [Relevant Tags]
- Content Type: [content-type]
- Learning Focus: [learning-focus-array]
- Difficulty: [beginner/intermediate/advanced]

**Evolutionary Project Fields:**
- project: "[Existing Project Name]"
- project_type: "evolutionary"
- evolution: "Evolution [X]: [Evolution Name]"
- evolution_number: [X]
- evolution_focus: "[Focus Area]"

**Content Requirements:**
- Write engaging, informative content
- Include evolution context at the beginning
- Add proper headings and structure
- Include code examples if relevant
- Add evolution navigation components

**Post Structure:**
- Introduction paragraph
- Evolution context block (using include)
- Main content with proper headings
- Code examples (if applicable)
- Key takeaways section
- Evolution posts component
- Post navigation component
- Conclusion

**Required Updates:**
1. **Update Project Hub:**
   - Add new post to the project overview in `_pages/projects/[project-name]/index.md`
   - Update post count and current status

2. **Update Evolution Page:**
   - Add new post to the specific evolution page in `_pages/projects/[project-name]/evolution-[X]/index.md`
   - Update post list and description

3. **Update Posts Timeline:**
   - Add new post to chronological timeline in `_pages/projects/[project-name]/posts/index.md`
   - Update post count and evolution summary

4. **Update Homepage:**
   - Update featured project section if this is the current active evolution
   - Update post count and status

5. **Update Evolution Navigation:**
   - Ensure cross-evolution links work correctly
   - Update evolution status if this completes an evolution

**File Location:**
- Create in `_posts/` directory with proper naming convention: `YYYY-MM-DD-post-title.md`

**Include Components:**
- Add `{% include evolution/post-navigation.html %}` at the end
- Add `{% include evolution/evolution-posts.html %}` before post navigation

**Cross-References:**
- Link to related posts in the same evolution
- Link to previous/next evolutions where appropriate
- Link back to project hub and evolution pages
```

---

## Usage Guidelines

### When to Use Each Prompt

1. **Generic Post**: Use for standalone content like tool reviews, general learning posts, or technology explorations
2. **New Project**: Use when starting a completely new evolutionary project with multiple planned phases
3. **Existing Evolution**: Use when adding posts to an already established evolutionary project

### Key Differences

- **Generic Post**: No evolution metadata, no project structure updates
- **New Project**: Creates entire project structure, updates homepage and projects page
- **Existing Evolution**: Updates existing project structure, maintains consistency

### Important Notes

- Always use the current date for new posts
- Follow the established naming convention for files
- Ensure all cross-references are updated
- Maintain consistency with existing project structure
- Include appropriate evolution context for project posts

### File Naming Convention

- Generic posts: `YYYY-MM-DD-post-title.md`
- Project posts: `YYYY-MM-DD-project-name-post-title.md`

### Evolution Status Indicators

- ✅ Complete: Evolution is finished
- 🔄 Active: Currently working on this evolution
- 📋 Planned: Future evolution

---

*This guide ensures consistent post creation and proper maintenance of the evolutionary project framework.*
