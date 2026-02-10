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

**Using user's context and guidance, agent creates complete post:**

#### File Content Structure
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

{AI-written content based on user's context and guidance}

## {Second Section Based on Type}

{AI-written content with examples, explanations, code snippets as appropriate}

## {Additional Sections Based on Type}

{Complete, engaging content ready to publish}
```

**Agent writes full content** based on:
- User's topic and context
- Post type template structure
- Professional, engaging tone
- Technical depth appropriate for the subject
- Code examples, explanations, and insights

### 5. User Review

**Inform user:**
```
✅ Created {post_type}: {filename}

Auto-populated:
  - Post type: {type}
  - Categories: {categories}
  - Structure: {sections based on type}
  - Series: {series name} (if applicable)

AI-written content:
  - {Section 1}: {brief description}
  - {Section 2}: {brief description}
  - Complete with examples and explanations

Ready for review and publishing!
```

## Configuration References

- Post types: `_data/config.yml → templates.generic_post.post_types`
- Series list: `_data/series.yml`
- Structure patterns: `_data/config.yml → templates.generic_post.structure`

## Examples

### Tutorial Post - Full Content Generation

```
USER: "Create generic post"
AGENT: "What type? [1] Tutorial [2] Deep Dive..."
USER: "1"
AGENT: "Title?"
USER: "Getting Started with Python Virtual Environments"
AGENT: "What should this cover? Key points?"
USER: "How to create venvs, activate them, install packages, and why they matter"
AGENT: "Part of a series? [1] Python Mastery [2] No"
USER: "1"

AGENT: ✅ Created: _posts/2026/02/2026-02-10-getting-started-python-virtual-environments.md

Complete tutorial written with:
  - Introduction: Why virtual environments matter
  - Prerequisites: Python 3.x installed
  - Step-by-Step Guide:
    * Creating a virtual environment
    * Activation commands (Windows/Mac/Linux)
    * Installing packages with pip
    * Managing requirements.txt
  - Conclusion: Best practices summary

Type: Tutorial
Categories: Tutorial, Learning
Series: Python Mastery

Ready to publish!
```

### Quick Tip - AI-Generated Content

```
USER: "Create generic post"
AGENT: "What type? [4] Quick Tip..."
USER: "4"
AGENT: "Title?"
USER: "VSCode Multi-Cursor Magic"
AGENT: "What's the tip?"
USER: "Ctrl+D to select next occurrence, great for bulk edits"

AGENT: ✅ Created: _posts/2026/02/2026-02-10-vscode-multi-cursor-magic.md

Complete quick tip written with:
  - The Problem: Repetitive edits across similar code
  - The Solution: Multi-cursor with Ctrl+D
  - How to Use: Step-by-step with examples

Type: Quick Tip
Categories: Quick Tips, Productivity

Ready to publish!
```

## Important Notes

- **Agent writes all content**, user provides topic and key points
- Posts are **complete and ready to publish** after generation
- User can still edit/refine as needed
- Agent should ask follow-up questions if context is insufficient
- Content should be engaging, informative, and well-structured
