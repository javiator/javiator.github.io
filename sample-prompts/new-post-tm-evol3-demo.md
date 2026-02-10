Create a new blog post for an EXISTING evolutionary project with the following requirements:

make relevant information from existing posts and setup if not provided correcly

**Post Details:**
- Title: Tenant Managememnt App Demo (webui)
- Date: 11th october
- Categories: [Relevant Categories]
- Tags: [Relevant Tags]
- Content Type: [content-type]
- Learning Focus: [learning-focus-array]
- Difficulty: [intermediate]

**Evolutionary Project Fields:**
- project: "[Tenant Management Evolution]"
- project_type: "evolutionary"
- evolution: "Evolution [3]: [Java Enterprise Stack]"
- evolution_number: [3]
- evolution_focus: "[Focus Area]"

**Content Requirements:**
- browse through the site running at localhost:. Go through different pages and take screenshot (read only). Perform some operation add transaction, click tenant details on tenant page - take screenshot. using various screenshot, define the post content of how tenant management applicaiton works and the way users can interact with it. 
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