---
name: create_generic_post
description: Create a standalone blog post not tied to any evolutionary project.
---

# Create Generic Post Skill

This skill creates a standard Jekyll blog post with intelligent post type detection and optional series association.

## Usage

Use this when creating standalone content: tutorials, deep dives, tool reviews, quick tips, or concept explanations.

## Intelligent Workflow

### 1. Gather Context

**Ask: "What type of post?"**
- [1] **Tutorial** - Step-by-step guide  
- [2] **Deep Dive** - Technical analysis/exploration
- [3] **Tool Review** - Tool evaluation and comparison
- [4] **Quick Tip** - Short productivity enhancer
- [5] **Concept Explanation** - Fundamental concept breakdown
- [6] **Other** - General post

**Ask: "Post title/topic?"**

**Ask: "Part of a content series?" (optional)**
- List available series from `_data/series.yml`
- Option: "No, standalone post"

### 2. Auto-Generate Based on Post Type

**Load template** from `_data/config.yml → templates.generic_post.post_types[selected_type]`

**Auto-populate:**
- **Categories**: From `suggested_categories` for post type
- **Structure**: Sections appropriate for post type
- **Date**: Current date (YYYY-MM-DD)
- **File path**: `_posts/YYYY/MM/YYYY-MM-DD-{post-slug}.md`

**Post Type Templates:**

#### Tutorial
- **Categories**: Tutorial, Learning
- **Structure**:
  - Introduction
  - Prerequisites
  - Step-by-Step Guide
  - Conclusion

#### Deep Dive
- **Categories**: Deep Dive, Technical
- **Structure**:
  - Introduction
  - Background
  - Technical Analysis
  - Insights and Learnings
  - Conclusion

#### Tool Review
- **Categories**: Tools, Reviews
- **Structure**:
  - Introduction
  - Overview
  - Key Features
  - Pros and Cons
  - Recommendation

#### Quick Tip
- **Categories**: Quick Tips, Productivity
- **Structure**:
  - The Problem
  - The Solution
  - How to Use

#### Concept Explanation
- **Categories**: Concepts, Fundamentals
- **Structure**:
  - Introduction
  - What is it?
  - Why does it matter?
  - How it works
  - Examples
  - Conclusion

### 3. Add Series Metadata (if applicable)

If user selected a series:
```yaml
series: "series-id"
series_order: [optional number]
```

### 4. Create File

**Determine path:**
- Pattern: `_posts/YYYY/MM/YYYY-MM-DD-{post-slug}.md`
- Create `_posts/YYYY/MM/` directory if needed

**File content template:**
```markdown
---
layout: post
title: "{title}"
date: YYYY-MM-DD
categories: [{suggested categories based on type}]
tags: [user-provided or suggested]
series: "{series-id}"  # If applicable
---

## {First Section Based on Type}

[User writes content]

## {Second Section Based on Type}

[User writes content]

...
```

### 5. User Guidance

**Inform user:**
```
✅ Created {post_type}: {filename}

Auto-populated:
  - Post type: {type}
  - Categories: {categories}
  - Structure: {sections based on type}
  - Series: {series name} (if applicable)

Ready for content!
```

## Configuration References

- Post types: `_data/config.yml → templates.generic_post.post_types`
- Series list: `_data/series.yml`
- Structure patterns: `_data/config.yml → templates.generic_post.structure`

## Examples

### Tutorial Post
```
USER: "Create generic post"
AGENT: "What type? [1] Tutorial [2] Deep Dive..."
USER: "1"
AGENT: "Title?"
USER: "Getting Started with Python Virtual Environments"
AGENT: "Part of a series? [1] Python Mastery [2] No"
USER: "1"
AGENT: ✅ Created: _posts/2026/02/2026-02-10-getting-started-python-virtual-environments.md
  - Type: Tutorial
  - Categories: Tutorial, Learning
  - Series: Python Mastery
  - Structure: Intro, Prerequisites, Step-by-Step, Conclusion
```

### Standalone Quick Tip
```
USER: "Create generic post"
AGENT: "What type? [1] Tutorial [2] Deep Dive [3] Tool Review [4] Quick Tip..."
USER: "4"
AGENT: "Title?"
USER: "VSCode Keyboard Shortcut for Multi-Cursor"
AGENT: "Part of a series? [1] No [2] ..."
USER: "1"
AGENT: ✅ Created: _posts/2026/02/2026-02-10-vscode-keyboard-shortcut-multi-cursor.md
  - Type: Quick Tip
  - Categories: Quick Tips, Productivity
  - Structure: Problem, Solution, How to Use
```
