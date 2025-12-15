Create a new blog post for an EXISTING evolutionary project with the following requirements:

make relevant information from existing posts and setup if not provided correcly

**Post Details:**
- Title: Tenant Managememnt Application with AI Conversational Interface
- Date: 7th Dec
- Categories: [Relevant Categories]
- Tags: [Relevant Tags]
- Content Type: [content-type]
- Learning Focus: [learning-focus-array]
- Difficulty: [intermediate]

**Evolutionary Project Fields:**
- project: "[Tenant Management Evolution]"
- project_type: "evolutionary"
- evolution: "Evolution [5]: [AI Conversational Interface in Application]"
- evolution_number: [5]
- evolution_focus: "[AI Conversational Interface in Application]"

**Content Requirements:**
- browse through the tenant-management-java-app application project that provides backend api for tenant management
- browse newly created ai conversational interface added into overall tenant management application
- browse existing posts to understand how various posts have been created and the current status of project
- browse via chrome site hosted on http://13.223.83.207/ to capture the new look and feel of website and capture images that can be then used in the post
- browse via chrome site hosted on http://13.223.83.207/ to capture the new coversational interface - try some messages like summary of all tenants for last 3 months, list all tenants with their contract expiring in next 3 months, etc. and capture images that can be then used in the post
- write a engaging post showcasing the enhancement of application with conversational interface. Elaborate on the idea on how this can simplify the user experience and provide more flexibility to users to explore data in their own way. Also highlight giving a dedicated page for AI Chat interface and how having a canvas for AI Chat allows a dedicated and intuitive way of sharing back the infromation with tables, graphs, charts etc. wihout polluting into the chat itself. Highlight how this could be best practice of providing engaging conversational interface to users without disrupting existing UI and user experience.
- Write engaging, informative content
- Include evolution context at the beginning
- Add proper headings and structure
- Include code examples if relevant
- Add evolution navigation components
- Make this post and the previous one as the featured post on home page

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