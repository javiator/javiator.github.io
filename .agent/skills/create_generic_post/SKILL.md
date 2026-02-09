---
name: create_generic_post
description: Create a standalone blog post not tied to any evolutionary project.
---

# Create Generic Post Skill

This skill creates a standard Jekyll blog post.

## Usage

Use this when the user wants to write a general article, tutorial, or update that is NOT part of a specific "Evolutionary Project".

## Steps

1.  **Determine Date and Title**:
    *   Get current date (YYYY-MM-DD).
    *   Slugify the title (e.g., "My New Post" -> "my-new-post").

2.  **Create Directory**:
    *   Ensure `_posts/YYYY/MM/` exists.

3.  **Create File**:
    *   Path: `_posts/YYYY/MM/YYYY-MM-DD-slug.md`

4.  **Content Template**:
    ```yaml
    ---
    layout: post
    title: "[Title]"
    date: YYYY-MM-DD
    categories: [Category1, Category2]
    tags: [tag1, tag2]
    # No project/evolution metadata
    ---

    Introduction...

    ## Heading

    Content...
    ```

5.  **remind user**:
    *   Remind them that this post will appear in the main feed but not in any project specific timelines.
